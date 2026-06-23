import re
from rank_bm25 import BM25Okapi


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class BM25Retriever:
    """Re-ranks an existing list of Pinecone match objects using BM25 scoring."""

    @staticmethod
    def rerank(query: str, matches: list, top_k: int = 5) -> list:
        if not matches:
            return []

        tokenized_corpus = [
            _tokenize(match.metadata.get("content", ""))
            for match in matches
        ]
        bm25 = BM25Okapi(tokenized_corpus)
        scores = bm25.get_scores(_tokenize(query))

        scored = sorted(zip(matches, scores), key=lambda x: x[1], reverse=True)
        return [match for match, _ in scored[:top_k]]
