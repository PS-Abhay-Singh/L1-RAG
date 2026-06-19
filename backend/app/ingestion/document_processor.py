from app.ingestion.pdf_loader import PDFLoader
from app.ingestion.metadata_extractor import MetadataExtractor
from app.ingestion.chunker import SectionChunker
from app.ingestion.recursive_chunker import RecursiveChunker

from app.embeddings.embedding_generator import EmbeddingGenerator
from app.vectordb.vector_store import VectorStore


class DocumentProcessor:

    @staticmethod
    def process(pdf_path: str):

        print("Loading PDF...")
        text = PDFLoader.load(pdf_path)

        print("Extracting Metadata...")
        metadata = MetadataExtractor.extract(text)

        print("Section Chunking...")
        section_chunks = SectionChunker.chunk(text)

        print("Recursive Chunking...")
        final_chunks = RecursiveChunker.chunk(section_chunks)

        print(f"Total Chunks: {len(final_chunks)}")

        records = []

        for chunk in final_chunks:

            embedding = EmbeddingGenerator.generate(
                chunk["content"]
            )

            record = {
                "id": f'{chunk["section"]}_{chunk["chunk_id"]}_{len(records)}',
                "values": embedding,
                "metadata": {
                    "paper_title": metadata["title"],
                    "section": chunk["section"],
                    "chunk_id": chunk["chunk_id"],
                    "content": chunk["content"]
                }
            }

            records.append(record)

        print("Uploading to Pinecone...")

        VectorStore.upsert_records(records)

        print("Done!")

        return {
            "paper_title": metadata["title"],
            "chunks": len(records)
        }