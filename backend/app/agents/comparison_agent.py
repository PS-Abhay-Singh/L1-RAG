from app.retrieval.fusion_retriever import FusionRetriever
from app.llm import get_llm


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
You are a Research Comparison Expert.

Using ONLY the provided context,
compare the technologies, frameworks,
or approaches mentioned.

Format:

# Overview

# Architecture Comparison

# Methodology Comparison

# Advantages

# Limitations

# Final Verdict

CONTEXT:

{context}

QUESTION:

{query}
"""

        response = llm.invoke(prompt)

        return response.content


def compare_papers(query: str):
    return ComparisonAgent.compare(query)