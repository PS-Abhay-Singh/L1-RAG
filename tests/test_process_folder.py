from backend.app.ingestion.document_processor import (
    DocumentProcessor
)

results = DocumentProcessor.process_folder(
    "data/pdfs"
)

print("\nSUMMARY")
print("=" * 50)

for result in results:

    print(
        f"{result['paper_title']} "
        f"-> {result['chunks']} chunks"
    )
