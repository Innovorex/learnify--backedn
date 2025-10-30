"""
Vector Store Service
Manages vector embeddings in Chroma DB for semantic search
Each teaching material gets its own collection for isolated search
"""

import os
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from services.text_chunker import TextChunk


class VectorStoreService:
    """
    Service for managing vector embeddings in Chroma DB
    Handles embedding generation, storage, and similarity search
    """

    def __init__(
        self,
        persist_directory: str = "./chroma_db_materials",
        embedding_model_name: str = "all-MiniLM-L6-v2"
    ):
        self.persist_directory = persist_directory
        self.embedding_model_name = embedding_model_name

        # Ensure directory exists
        os.makedirs(persist_directory, exist_ok=True)

        # Initialize Chroma client - use existing instance if available
        try:
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
        except Exception as e:
            # If client already exists, get the existing one
            print(f"[VECTOR STORE] Reusing existing Chroma client: {e}")
            self.client = chromadb.PersistentClient(path=persist_directory)

        # Initialize embedding model
        print(f"Loading embedding model: {embedding_model_name}...")
        self.embedding_model = SentenceTransformer(embedding_model_name)
        print(f"✅ Vector Store initialized with {embedding_model_name}")

    def create_material_collection(
        self,
        material_id: int
    ) -> str:
        """
        Create a new collection for a teaching material
        Returns: collection_name
        """
        collection_name = f"material_{material_id}"

        try:
            # Delete existing collection if exists
            try:
                self.client.delete_collection(name=collection_name)
                print(f"🗑️  Deleted existing collection: {collection_name}")
            except:
                pass

            # Create new collection
            collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}  # Use cosine similarity
            )

            print(f"✅ Created collection: {collection_name}")
            return collection_name

        except Exception as e:
            raise Exception(f"Failed to create collection: {str(e)}")

    def add_chunks_to_collection(
        self,
        collection_name: str,
        chunks: List[TextChunk],
        material_id: int
    ) -> List[str]:
        """
        Add text chunks to collection with embeddings
        Returns: list of chroma_ids
        """
        try:
            collection = self.client.get_collection(name=collection_name)

            # Prepare data
            texts = [chunk.text for chunk in chunks]
            ids = [f"{material_id}_chunk_{chunk.chunk_index}" for chunk in chunks]

            metadatas = [
                {
                    "material_id": material_id,
                    "chunk_index": chunk.chunk_index,
                    "char_count": chunk.char_count,
                    "token_estimate": chunk.token_estimate,
                    "page_number": chunk.page_number or 0,
                    "section_title": chunk.section_title or ""
                }
                for chunk in chunks
            ]

            # Generate embeddings
            print(f"Generating embeddings for {len(texts)} chunks...")
            embeddings = self.embedding_model.encode(
                texts,
                show_progress_bar=True,
                convert_to_numpy=True
            ).tolist()

            # Add to collection in batches (Chroma has limits)
            batch_size = 100
            for i in range(0, len(texts), batch_size):
                batch_end = min(i + batch_size, len(texts))

                collection.add(
                    embeddings=embeddings[i:batch_end],
                    documents=texts[i:batch_end],
                    metadatas=metadatas[i:batch_end],
                    ids=ids[i:batch_end]
                )

            print(f"✅ Added {len(chunks)} chunks to {collection_name}")
            return ids

        except Exception as e:
            raise Exception(f"Failed to add chunks to collection: {str(e)}")

    def search_similar_chunks(
        self,
        collection_name: str,
        query: str,
        n_results: int = 5,
        where_filter: Optional[Dict] = None
    ) -> Dict:
        """
        Search for similar chunks using semantic search
        Returns: {
            'ids': [[]],
            'documents': [[]],
            'metadatas': [[]],
            'distances': [[]]
        }
        """
        try:
            collection = self.client.get_collection(name=collection_name)

            # Generate query embedding
            query_embedding = self.embedding_model.encode([query], convert_to_numpy=True)[0].tolist()

            # Search
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_filter,
                include=["documents", "metadatas", "distances"]
            )

            return results

        except Exception as e:
            raise Exception(f"Failed to search collection '{collection_name}': {str(e)}")

    def get_all_chunks(
        self,
        collection_name: str,
        limit: int = 100
    ) -> Dict:
        """
        Get all chunks from a collection (for exam generation)
        Returns: {
            'ids': [],
            'documents': [],
            'metadatas': []
        }
        """
        try:
            collection = self.client.get_collection(name=collection_name)

            # Get all documents
            results = collection.get(
                limit=limit,
                include=["documents", "metadatas"]
            )

            return results

        except Exception as e:
            raise Exception(f"Failed to get chunks from collection: {str(e)}")

    def get_chunks_by_ids(
        self,
        collection_name: str,
        chunk_ids: List[str]
    ) -> Dict:
        """
        Retrieve specific chunks by their IDs
        """
        try:
            collection = self.client.get_collection(name=collection_name)

            results = collection.get(
                ids=chunk_ids,
                include=["documents", "metadatas"]
            )

            return results

        except Exception as e:
            raise Exception(f"Failed to retrieve chunks: {str(e)}")

    def delete_material_collection(self, collection_name: str):
        """Delete a material's collection"""
        try:
            self.client.delete_collection(name=collection_name)
            print(f"✅ Deleted collection: {collection_name}")
        except Exception as e:
            print(f"⚠️  Failed to delete collection {collection_name}: {e}")

    def collection_exists(self, collection_name: str) -> bool:
        """Check if a collection exists"""
        try:
            self.client.get_collection(name=collection_name)
            return True
        except:
            return False

    def get_collection_info(self, collection_name: str) -> Dict:
        """Get information about a collection"""
        try:
            collection = self.client.get_collection(name=collection_name)
            count = collection.count()

            return {
                "name": collection_name,
                "count": count,
                "metadata": collection.metadata,
                "exists": True
            }
        except Exception as e:
            return {
                "name": collection_name,
                "exists": False,
                "error": str(e)
            }


# Global instance (initialized once)
_vector_store_instance = None


def get_vector_store() -> VectorStoreService:
    """Get or create the global vector store instance"""
    global _vector_store_instance

    if _vector_store_instance is None:
        _vector_store_instance = VectorStoreService()

    return _vector_store_instance
