import os

from backend.app.ingestion.pdf_loader import PDFLoader
from backend.app.ingestion.metadata_extractor import MetadataExtractor
from backend.app.ingestion.chunker import SectionChunker
from backend.app.ingestion.recursive_chunker import RecursiveChunker

from backend.app.embeddings.embedding_generator import EmbeddingGenerator
from backend.app.vectordb.vector_store import VectorStore


class DocumentProcessor:

    @staticmethod
    def process(pdf_path: str):

        print(f"\nProcessing: {pdf_path}")

        # -----------------------------
        # Load PDF
        # -----------------------------

        print("Loading PDF...")
        text = PDFLoader.load(pdf_path)

        # Safety Check 1
        if not text or not text.strip():
            raise Exception(
                f"No text extracted from {pdf_path}"
            )

        # -----------------------------
        # Extract Metadata
        # -----------------------------

        print("Extracting Metadata...")
        metadata = MetadataExtractor.extract(text, pdf_path)

        # Fallback title
        if not metadata.get("title"):
            metadata["title"] = os.path.basename(
                pdf_path
            ).replace(".pdf", "")

        # -----------------------------
        # Section Chunking
        # -----------------------------

        print("Section Chunking...")
        section_chunks = SectionChunker.chunk(text)

        if len(section_chunks) == 0:
            raise Exception(
                f"No sections extracted from {pdf_path}"
            )

        # -----------------------------
        # Recursive Chunking
        # -----------------------------

        print("Recursive Chunking...")
        final_chunks = RecursiveChunker.chunk(
            section_chunks
        )

        print(f"Total Chunks: {len(final_chunks)}")

        # Safety Check 2
        if len(final_chunks) == 0:
            raise Exception(
                f"No chunks created from {pdf_path}"
            )

        # -----------------------------
        # Create Pinecone Records
        # -----------------------------

        records = []

        for idx, chunk in enumerate(final_chunks):

            embedding = EmbeddingGenerator.generate(
                chunk["content"]
            )

            record = {
                "id": f"{metadata['title']}_{idx}",
                "values": embedding,
                "metadata": {
                    "paper_title": metadata["title"],
                    "source_file": os.path.basename(
                        pdf_path
                    ),
                    "section": chunk["section"],
                    "chunk_id": chunk["chunk_id"],
                    "content": chunk["content"]
                }
            }

            records.append(record)

        # Safety Check 3
        if len(records) == 0:
            raise Exception(
                f"No vectors generated from {pdf_path}"
            )

        # -----------------------------
        # Upload To Pinecone
        # -----------------------------

        print("Uploading to Pinecone...")

        VectorStore.upsert_records(
            records
        )

        print("Done!")

        return {
            "paper_title": metadata["title"],
            "source_file": os.path.basename(
                pdf_path
            ),
            "chunks": len(records)
        }

    @staticmethod
    def process_folder(folder_path: str):

        results = []

        pdf_files = [
            file
            for file in os.listdir(folder_path)
            if file.endswith(".pdf")
        ]

        print(
            f"\nFound {len(pdf_files)} PDF files"
        )

        for filename in pdf_files:

            pdf_path = os.path.join(
                folder_path,
                filename
            )

            try:

                result = DocumentProcessor.process(
                    pdf_path
                )

                results.append(result)

            except Exception as e:

                print(
                    f"\nFailed to process {filename}"
                )

                print(
                    f"Reason: {str(e)}"
                )

        return results