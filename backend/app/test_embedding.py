from app.embeddings.embedding_generator import EmbeddingGenerator

embedding = EmbeddingGenerator.generate(
    "GraphRAG improves retrieval using graph structures."
)

print("DIMENSIONS:", len(embedding))

print("FIRST 10 VALUES:")
print(embedding[:10])