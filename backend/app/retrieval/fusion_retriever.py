from backend.app.retrieval.multi_query_retriever import MultiQueryRetriever
from backend.app.retrieval.bm25_retriever import BM25Retriever
from backend.app.retrieval.rrf import RRF


class FusionRetriever:

    @staticmethod
    def retrieve(query: str, top_k: int = 5) -> list:
        """MultiQuery vector search → RRF fusion → BM25 re-rank."""
        multi_results = MultiQueryRetriever.retrieve(query)

        fused = RRF.fuse(multi_results)

        return BM25Retriever.rerank(query, fused, top_k=top_k)
