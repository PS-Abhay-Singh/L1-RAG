from backend.app.ingestion.pdf_loader import PDFLoader
from backend.app.ingestion.chunker import SectionChunker

text = PDFLoader.load("data/pdfs/GraphRAG.pdf")

sections = SectionChunker.chunk(text)

for section in sections:
    print("=" * 50)
    print("SECTION:")
    print(repr(section["section"]))
