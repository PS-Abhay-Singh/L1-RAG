class RecursiveChunker:
    """Simple recursive text chunker without heavy dependencies"""

    @staticmethod
    def chunk(section_chunks, chunk_size=1000, chunk_overlap=200):
        """
        Recursively split text into chunks.
        
        Args:
            section_chunks: List of dicts with 'section' and 'content' keys
            chunk_size: Maximum size of each chunk
            chunk_overlap: Number of characters to overlap between chunks
        
        Returns:
            List of chunk dictionaries with 'section', 'chunk_id', 'content'
        """
        final_chunks = []

        for section_chunk in section_chunks:
            section_name = section_chunk["section"]
            content = section_chunk["content"]

            # Simple recursive chunking
            chunks = RecursiveChunker._split_text(
                content, chunk_size, chunk_overlap
            )

            for idx, chunk in enumerate(chunks):
                final_chunks.append(
                    {
                        "section": section_name,
                        "chunk_id": idx,
                        "content": chunk
                    }
                )

        return final_chunks

    @staticmethod
    def _split_text(text, chunk_size=1000, chunk_overlap=200):
        """Simple recursive text splitter"""
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            if end < len(text):
                last_period = text.rfind(".", start, end)
                last_exclaim = text.rfind("!", start, end)
                last_question = text.rfind("?", start, end)
                last_newline = text.rfind("\n", start, end)

                split_pos = max(last_period, last_exclaim, last_question, last_newline)

                # Only use boundary if it actually advances past start
                if split_pos > start + chunk_overlap:
                    end = split_pos + 1

            chunks.append(text[start:end].strip())
            next_start = end - chunk_overlap

            # Guard: always move forward to prevent infinite loop
            if next_start <= start:
                next_start = start + chunk_size
            start = next_start

        return [c for c in chunks if c]
