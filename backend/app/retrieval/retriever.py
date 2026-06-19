from app.embeddings.embedding_generator import EmbeddingGenerator
from app.vectordb.pinecone_client import index


class Retriever:

    @staticmethod
    def retrieve(
        query: str,
        top_k: int = 5
    ):

        query_embedding = EmbeddingGenerator.generate(
            query
        )

        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        return results