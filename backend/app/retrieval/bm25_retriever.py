from rank_bm25 import BM25Okapi


class BM25Retriever:
    """Re-ranks an existing list of Pinecone match objects using BM25 scoring."""

    @staticmethod
    def rerank(query: str, matches: list, top_k: int = 5) -> list:
        if not matches:
            return []

        tokenized_corpus = [
            match.metadata.get("content", "").lower().split()
            for match in matches
        ]
        query_tokens = query.lower().split()

        bm25 = BM25Okapi(tokenized_corpus)
        scores = bm25.get_scores(query_tokens)

        scored = sorted(zip(matches, scores), key=lambda x: x[1], reverse=True)
        return [match for match, _ in scored[:top_k]]
