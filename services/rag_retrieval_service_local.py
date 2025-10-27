import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from services.model_config import CHROMA_DB_PATH, EMBEDDING_MODEL, COLLECTION_NAME

class RAGRetrievalServiceLocal:
    def __init__(self, chroma_db_path: str = CHROMA_DB_PATH):
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=chroma_db_path)

        # Initialize FREE local embedding function
        self.embedding_function = SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )

        # Get collection
        self.collection = self.client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=self.embedding_function
        )

        doc_count = self.collection.count()
        print(f"[RAG RETRIEVAL] Connected to collection '{COLLECTION_NAME}'")
        print(f"[RAG RETRIEVAL] Collection has {doc_count} documents")

    def retrieve_for_ai_tutor(
        self,
        teacher_question: str,
        subject: str,
        grade: str,
        is_bed_qualified: bool,
        top_k: int = 5
    ) -> dict:
        """
        Retrieve relevant pedagogy content for AI Tutor
        """
        # Build enhanced query
        if is_bed_qualified:
            # B.Ed qualified - focus on subject depth
            enhanced_query = f"{subject} teaching methodology for Grade {grade}: {teacher_question}"
        else:
            # Non-B.Ed - focus on HOW to teach
            enhanced_query = f"How to teach {subject} to Grade {grade} students: {teacher_question}. Teaching methods, pedagogical approaches, classroom strategies."

        print(f"[RAG RETRIEVAL] Query: {enhanced_query[:100]}...")

        # Query ChromaDB (embeddings generated automatically)
        results = self.collection.query(
            query_texts=[enhanced_query],
            n_results=top_k
        )

        # Format results
        pedagogy_chunks = []
        if results and results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i]
                distance = results['distances'][0][i]
                relevance = 1 - distance  # Convert distance to relevance

                pedagogy_chunks.append({
                    "content": doc,
                    "module": metadata.get("module", "Unknown"),
                    "subject": metadata.get("subject", "Unknown"),
                    "file_name": metadata.get("file_name", "Unknown"),
                    "relevance": round(relevance, 3)
                })

                print(f"[RAG RETRIEVAL] Result {i+1}: {metadata.get('module')} - Relevance: {relevance:.3f}")

        return {
            "query": enhanced_query,
            "results": pedagogy_chunks,
            "count": len(pedagogy_chunks)
        }

# Initialize service
rag_retrieval_service_local = RAGRetrievalServiceLocal()
