from ..llm.ollama_client import get_llm

def understand_query(query: str):

    llm = get_llm()

    prompt = f"""
You are a Query Understanding Agent.

Analyze the query.

Return ONLY valid JSON.

Format:

{{
    "intent": "",
    "topics": [],
    "query_type": ""
}}

Query:
{query}
"""

    response = llm.invoke(prompt)

    return response.content