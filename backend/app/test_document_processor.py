from app.ingestion.document_processor import DocumentProcessor

result = DocumentProcessor.process(
    "data/pdfs/GraphRAG.pdf"
)

print(result)