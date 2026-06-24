from backend.app.retrieval.fusion_retriever import FusionRetriever
from backend.app.agents.answer_generation import generate_answer, _is_summarization
from backend.app.retrieval.retriever import Retriever
from backend.app.retrieval.bm25_retriever import BM25Retriever


class RAGPipeline:

    @staticmethod
    def _retrieve(query: str) -> list:
        if _is_summarization(query):
            # Broad sweep — top-20 by vector similarity covers more of the doc
            results = Retriever.retrieve(query, top_k=20)
            matches = results.get("matches", [])
            return BM25Retriever.rerank(query, matches, top_k=15)
        return FusionRetriever.retrieve(query, top_k=5)

    @staticmethod
    def ask(query: str):
        results = RAGPipeline._retrieve(query)
        context = "\n\n".join(m.metadata["content"] for m in results)
        return generate_answer(query=query, context=context)

    @staticmethod
    def ask_with_sources(query: str):
        results = RAGPipeline._retrieve(query)
        context = "\n\n".join(m.metadata["content"] for m in results)
        answer = generate_answer(query=query, context=context)
        return answer, results