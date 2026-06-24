from backend.app.retrieval.fusion_retriever import FusionRetriever
from backend.app.llm import get_llm


class ResearchAgent:

    @staticmethod
    def analyze(query: str):

        results = FusionRetriever.retrieve(query)

        context = "\n\n".join(
            [
                match.metadata["content"]
                for match in results
            ]
        )

        llm = get_llm()

        prompt = f"""
You are a Document Analyst.

Using ONLY the provided context, answer the question with a structured analysis.
Adapt your response format to the type of content — it may be a research paper,
technical manual, legal document, report, book chapter, or any other document type.

Provide a clear, well-structured response with relevant headings based on what
the content actually contains.

CONTEXT:

{context}

QUESTION:

{query}
"""

        response = llm.invoke(prompt)

        return response.content