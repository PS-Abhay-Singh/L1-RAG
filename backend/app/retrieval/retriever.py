from app.embeddings.embedding_generator import EmbeddingGenerator
from app.vectordb.pinecone_client import index


class Retriever:

    @staticmethod
    def retrieve(
        query: str,
        top_k: int = 5,
        selected_papers=None
    ):

        query_embedding = EmbeddingGenerator.generate(
            query
        )

        query_params = {
            "vector": query_embedding,
            "top_k": top_k,
            "include_metadata": True
        }

        if selected_papers:

            query_params["filter"] = {
                "paper_title": {
                    "$in": selected_papers
                }
            }

        results = index.query(
            **query_params
        )

        return results