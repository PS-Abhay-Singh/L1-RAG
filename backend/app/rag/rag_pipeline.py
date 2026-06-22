from app.retrieval.fusion_retriever import FusionRetriever
from app.agents.answer_generation import generate_answer


class RAGPipeline:

    @staticmethod
    def ask(query: str):

        results = FusionRetriever.retrieve(
            query
        )

        context = "\n\n".join(
            [
                match.metadata["content"]
                for match in results
            ]
        )

        answer = generate_answer(
            query=query,
            context=context
        )

        return answer