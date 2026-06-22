from backend.app.retrieval.retriever import Retriever
from backend.app.retrieval.bm25_retriever import BM25Retriever
from collections import defaultdict


class HybridRetriever:
    """Hybrid retrieval: vector search + BM25 re-rank."""

    @staticmethod
    def retrieve(query: str, vector_weight: float = 0.6, bm25_weight: float = 0.4) -> list:
        vector_results = Retriever.retrieve(query, top_k=10)
        matches = vector_results.get("matches", [])

        bm25_reranked = BM25Retriever.rerank(query, matches, top_k=10)

        scores = defaultdict(float)
        documents = {}

        for rank, match in enumerate(matches):
            scores[match.id] += vector_weight * (1.0 / (rank + 1))
            documents[match.id] = match

        for rank, match in enumerate(bm25_reranked):
            scores[match.id] += bm25_weight * (1.0 / (rank + 1))
            documents[match.id] = match

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [documents[doc_id] for doc_id, _ in ranked[:5]]
