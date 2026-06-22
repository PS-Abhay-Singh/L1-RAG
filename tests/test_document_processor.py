from backend.app.ingestion.document_processor import DocumentProcessor

result = DocumentProcessor.process(
    "data/pdfs/AgenticRAG.pdf"
)

print(result)
