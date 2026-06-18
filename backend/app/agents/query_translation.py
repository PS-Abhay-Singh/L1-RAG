from langchain_core.prompts import ChatPromptTemplate
from ..llm import get_llm


def translate_query(query: str):

    llm = get_llm()

    prompt = f"""
    You are a Query Translation Agent.

    Generate search queries that will help retrieve
    research papers related to the user query.

    Return ONLY a valid JSON array.

    Example:

    [
        "GraphRAG architecture",
        "GraphRAG advantages"
    ]

    Query:
    {query}
    """

    response = llm.invoke(prompt)

    return response.content
