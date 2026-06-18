from ..llm.ollama_client import get_llm


def understand_query(query: str):

    llm = get_llm()

    prompt = f"""
    You are a Query Understanding Agent.

    Analyze the query and identify:

    1. Intent
    2. Topics
    3. Query Type

    Query:
    {query}
    """

    response = llm.invoke(prompt)

    return response.content