from app.ingestion.pdf_loader import PDFLoader
from app.ingestion.chunker import SectionChunker
from app.ingestion.recursive_chunker import RecursiveChunker

pdf_path = "data/pdfs/GraphRAG.pdf"

text = PDFLoader.load(pdf_path)

section_chunks = SectionChunker.chunk(text)

print(f"SECTION CHUNKS: {len(section_chunks)}")

final_chunks = RecursiveChunker.chunk(section_chunks)

print(f"FINAL CHUNKS: {len(final_chunks)}")

print("=" * 50)

print(final_chunks[0])