from langchain_text_splitters import RecursiveCharacterTextSplitter


class RecursiveChunker:

    @staticmethod
    def chunk(section_chunks):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        final_chunks = []

        for section_chunk in section_chunks:

            section_name = section_chunk["section"]
            content = section_chunk["content"]

            chunks = splitter.split_text(content)

            for idx, chunk in enumerate(chunks):

                final_chunks.append(
                    {
                        "section": section_name,
                        "chunk_id": idx,
                        "content": chunk
                    }
                )

        return final_chunks