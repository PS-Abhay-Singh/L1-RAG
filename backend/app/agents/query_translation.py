from langchain_core.prompts import ChatPromptTemplate
from ..llm import get_llm
import json


def translate_query(query: str):

    llm = get_llm()

    prompt = f"""
    You are a Query Translation Agent.

    Generate 4 diverse search queries.

Each query should explore a different aspect:

1. Definition
2. Architecture
3. Methodology
4. Advantages / Evaluation

    Return ONLY a JSON array.

    Example:

    [
        "GraphRAG architecture",
        "GraphRAG advantages"
    ]

    Query:
    {query}
    """

    response = llm.invoke(prompt)

    try:
        return json.loads(response.content)
    except:
        return [query]