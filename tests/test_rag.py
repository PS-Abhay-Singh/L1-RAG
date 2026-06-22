from backend.app.rag.rag_pipeline import RAGPipeline

response = RAGPipeline.ask(
    "What is HiRAG?"
)

print(response)
