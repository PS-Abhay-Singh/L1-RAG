from backend.app.retrieval.fusion_retriever import FusionRetriever
from backend.app.llm import get_llm


class ComparisonAgent:

    @staticmethod
    def compare(query: str):

        results = FusionRetriever.retrieve(query)

        context = "\n\n".join(
            [
                match.metadata["content"]
                for match in results
            ]
        )

        llm = get_llm()

        prompt = f"""
You are a Document Comparison Expert.

Using ONLY the provided context, compare the topics, entities, approaches,
or items mentioned in the question.
Adapt your comparison structure to the actual content — it may be research papers,
products, legal clauses, processes, or any other type of document content.

Provide a clear structured comparison with headings relevant to what is being compared.
End with a summary or verdict.

CONTEXT:

{context}

QUESTION:

{query}
"""

        response = llm.invoke(prompt)

        return response.content


def compare_papers(query: str):
    return ComparisonAgent.compare(query)