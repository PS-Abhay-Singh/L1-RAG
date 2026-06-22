from app.retrieval.fusion_retriever import FusionRetriever
from app.llm import get_llm


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
You are a Research Analyst.

Using ONLY the provided context,
generate a structured research analysis.

Format:

# Topic

# Problem Being Solved

# Proposed Solution

# Methodology

# Advantages

# Limitations

CONTEXT:

{context}

QUESTION:

{query}
"""

        response = llm.invoke(prompt)

        return response.content