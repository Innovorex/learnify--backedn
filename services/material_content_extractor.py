"""
Material Content Extractor Service
===================================
Extracts content from teaching materials for question generation.
Retrieves specific page ranges from vector store.
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from services.vector_store_service import get_vector_store


def extract_material_content(
    material_id: int,
    from_page: int,
    to_page: int,
    db: Session
) -> str:
    """
    Extract content from teaching material for specific page range

    Args:
        material_id: ID of the teaching material
        from_page: Starting page number (inclusive)
        to_page: Ending page number (inclusive)
        db: Database session

    Returns:
        Concatenated text content from the specified pages

    Raises:
        ValueError: If material not found or no content in page range
    """
    try:
        # Get material info from database
        result = db.execute(
            text("SELECT title, original_filename FROM teaching_materials WHERE id = :material_id"),
            {"material_id": material_id}
        ).fetchone()

        if not result:
            raise ValueError(f"Material {material_id} not found")

        material_title, filename = result
        print(f"[MATERIAL EXTRACT] Material: {material_title} ({filename})")

        # Get from vector store
        vector_store = get_vector_store()
        collection_name = f"material_{material_id}"

        if not vector_store.collection_exists(collection_name):
            raise ValueError(f"Material collection not found for material {material_id}")

        # Get collection
        collection = vector_store.client.get_collection(collection_name)

        # Get all chunks from collection
        all_chunks = collection.get()

        if not all_chunks or not all_chunks['documents']:
            raise ValueError(f"No content found in material {material_id}")

        # Filter chunks by page range
        relevant_content = []
        page_numbers_found = set()

        for idx, metadata in enumerate(all_chunks['metadatas']):
            page_num = metadata.get('page_number', 0)

            # Convert page_num to int if it's a string
            try:
                page_num = int(page_num)
            except (ValueError, TypeError):
                page_num = 0

            # Check if page is in range
            if from_page <= page_num <= to_page:
                content = all_chunks['documents'][idx]
                relevant_content.append(f"[Page {page_num}]\n{content}")
                page_numbers_found.add(page_num)

        if not relevant_content:
            raise ValueError(
                f"No content found in pages {from_page}-{to_page}. "
                f"Material may not have content in this page range."
            )

        # Sort by page number
        relevant_content_sorted = sorted(
            zip(page_numbers_found, relevant_content),
            key=lambda x: x[0]
        )

        # Concatenate all content
        full_content = "\n\n".join([content for _, content in relevant_content_sorted])

        print(f"[MATERIAL EXTRACT] Extracted {len(relevant_content)} chunks from pages {from_page}-{to_page}")
        print(f"[MATERIAL EXTRACT] Pages found: {sorted(page_numbers_found)}")
        print(f"[MATERIAL EXTRACT] Total characters: {len(full_content)}")

        return full_content

    except Exception as e:
        print(f"[MATERIAL EXTRACT ERROR] {e}")
        raise
