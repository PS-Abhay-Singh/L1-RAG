from backend.app.llm import get_llm
import json


class PaperSelectionAgent:

    @staticmethod
    def select(query: str):

        llm = get_llm()

        prompt = f"""
You are a Paper Selection Agent.

Available papers:

1. HiRAG
2. LightRAG

Determine which papers are relevant.

Return ONLY JSON.

Example:

["HiRAG"]

or

["HiRAG", "LightRAG"]

Query:
{query}
"""

        response = llm.invoke(prompt)

        try:
            return json.loads(
                response.content
            )

        except:
            return []