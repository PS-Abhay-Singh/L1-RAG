from ..llm import get_llm
import json
import re


def _extract_json_array(text: str):
    text = re.sub(r"```(?:json)?", "", text).strip()
    try:
        result = json.loads(text)
        if isinstance(result, list):
            return [str(q) for q in result if q]
    except Exception:
        pass
    # Try extracting first [...] block
    match = re.search(r"\[.*?\]", text, re.DOTALL)
    if match:
        try:
            result = json.loads(match.group())
            if isinstance(result, list):
                return [str(q) for q in result if q]
        except Exception:
            pass
    return []


def translate_query(query: str):

    llm = get_llm()

    prompt = f"""
    You are a Query Translation Agent.

    Generate 4 diverse search queries that explore different aspects of the topic.
    The document may be a research paper, report, manual, contract, book, or any other type.
    Adapt the sub-queries to best retrieve relevant information for the given query.
    IMPORTANT: Base sub-queries ONLY on the original query — do not add outside knowledge.

    Return ONLY a JSON array of 4 strings. No explanation, no markdown.

    Query:
    {query}
    """

    response = llm.invoke(prompt)
    queries = _extract_json_array(response.content)
    return queries if queries else [query]