"""
Text Chunking Service
Splits large text into smaller segments for embedding and vector search
Uses semantic chunking with overlap for better context preservation
"""

import re
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class TextChunk:
    """Represents a chunk of text with metadata"""
    text: str
    chunk_index: int
    page_number: int = None
    section_title: str = None
    char_count: int = 0
    token_estimate: int = 0


class TextChunkerService:
    """
    Service for chunking large text into smaller segments for embedding
    Uses semantic chunking with overlap for better context preservation
    """

    def __init__(
        self,
        chunk_size: int = 1000,  # Characters per chunk
        chunk_overlap: int = 200,  # Overlap between chunks
        min_chunk_size: int = 100  # Minimum chunk size
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size

    def chunk_text(
        self,
        text: str,
        page_metadata: Dict = None
    ) -> List[TextChunk]:
        """
        Main chunking function
        Returns list of TextChunk objects
        """
        if not text or not text.strip():
            return []

        # Try semantic chunking first (by paragraphs/sections)
        semantic_chunks = self._semantic_chunk(text)

        # If semantic chunks are too large, use sliding window
        final_chunks = []
        chunk_index = 0

        for semantic_chunk in semantic_chunks:
            if len(semantic_chunk) <= self.chunk_size:
                # Chunk is good size, use as-is
                final_chunks.append(TextChunk(
                    text=semantic_chunk,
                    chunk_index=chunk_index,
                    char_count=len(semantic_chunk),
                    token_estimate=self._estimate_tokens(semantic_chunk)
                ))
                chunk_index += 1
            else:
                # Chunk too large, split with sliding window
                sliding_chunks = self._sliding_window_chunk(semantic_chunk)
                for sliding_chunk in sliding_chunks:
                    final_chunks.append(TextChunk(
                        text=sliding_chunk,
                        chunk_index=chunk_index,
                        char_count=len(sliding_chunk),
                        token_estimate=self._estimate_tokens(sliding_chunk)
                    ))
                    chunk_index += 1

        return final_chunks

    def _semantic_chunk(self, text: str) -> List[str]:
        """
        Chunk by semantic units (paragraphs, sections)
        Preserves natural text boundaries
        """
        # Split by double newlines (paragraphs)
        paragraphs = re.split(r'\n\s*\n', text)

        chunks = []
        current_chunk = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # If adding this paragraph exceeds chunk size, save current chunk
            if len(current_chunk) + len(para) + 1 > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                # Start new chunk with overlap
                overlap_text = self._get_overlap_text(current_chunk)
                current_chunk = overlap_text + " " + para if overlap_text else para
            else:
                current_chunk += "\n\n" + para if current_chunk else para

        # Add remaining chunk
        if current_chunk and len(current_chunk.strip()) >= self.min_chunk_size:
            chunks.append(current_chunk.strip())

        return chunks if chunks else [text]  # Return original if no chunks created

    def _sliding_window_chunk(self, text: str) -> List[str]:
        """
        Split text using sliding window with overlap
        Used when semantic chunks are too large
        """
        chunks = []
        start = 0
        text_len = len(text)

        while start < text_len:
            end = start + self.chunk_size

            # Try to break at sentence boundary
            if end < text_len:
                # Look for sentence end within next 100 chars
                search_end = min(end + 100, text_len)
                sentence_breaks = [m.end() for m in re.finditer(r'[.!?]\s+', text[end:search_end])]
                if sentence_breaks:
                    end = end + sentence_breaks[0]

            chunk = text[start:end].strip()

            if len(chunk) >= self.min_chunk_size:
                chunks.append(chunk)

            # Move start position with overlap
            start = end - self.chunk_overlap
            if start >= text_len:
                break

        return chunks if chunks else [text]

    def _get_overlap_text(self, text: str) -> str:
        """Get last N characters for overlap"""
        if len(text) <= self.chunk_overlap:
            return text
        return text[-self.chunk_overlap:]

    def _estimate_tokens(self, text: str) -> int:
        """
        Estimate token count (rough approximation)
        1 token ≈ 4 characters for English
        """
        return len(text) // 4

    def extract_sections(self, text: str) -> List[tuple]:
        """
        Extract sections with titles
        Returns: [(section_title, section_text), ...]
        """
        sections = []

        # Pattern to match section headers (e.g., "1. Introduction", "Chapter 1:", etc.)
        section_pattern = r'^(?:Chapter\s+\d+|Section\s+\d+|\d+\.|\d+\.\d+|[A-Z][A-Z\s]{2,}):?\s*(.+)?$'

        lines = text.split('\n')
        current_section = None
        current_text = []

        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue

            match = re.match(section_pattern, line_stripped, re.IGNORECASE)
            if match:
                # Save previous section
                if current_section:
                    sections.append((current_section, '\n'.join(current_text)))

                # Start new section
                current_section = line_stripped
                current_text = []
            else:
                current_text.append(line)

        # Save last section
        if current_section:
            sections.append((current_section, '\n'.join(current_text)))

        return sections

    def chunk_with_page_info(
        self,
        text: str,
        page_texts: Dict[int, str]
    ) -> List[TextChunk]:
        """
        Chunk text and associate chunks with page numbers
        page_texts: {page_num: text_on_that_page}
        """
        # Create chunks normally
        chunks = self.chunk_text(text)

        # Try to assign page numbers to chunks
        page_boundaries = []
        char_count = 0
        for page_num in sorted(page_texts.keys()):
            page_text = page_texts[page_num]
            char_count += len(page_text)
            page_boundaries.append((char_count, page_num))

        # Assign page numbers to chunks
        char_position = 0
        for chunk in chunks:
            chunk_start = char_position
            chunk_end = char_position + len(chunk.text)
            chunk_middle = (chunk_start + chunk_end) // 2

            # Find which page this chunk belongs to
            for boundary, page_num in page_boundaries:
                if chunk_middle <= boundary:
                    chunk.page_number = page_num
                    break

            char_position = chunk_end

        return chunks
