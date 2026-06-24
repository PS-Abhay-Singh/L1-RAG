import json
import re
from ..llm.ollama_client import get_llm

_VALID_QUERY_TYPES = {"research", "comparison", "summary", "factual", "general"}

_FALLBACK = {"intent": "general", "topics": [], "query_type": "general"}


def _extract_json(text: str) -> dict:
    # Strip markdown code fences if present
    text = re.sub(r"```(?:json)?", "", text).strip()
    try:
        return json.loads(text)
    except Exception:
        # Try extracting first {...} block
        match = re.search(r"\{.*?\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
    return {}


def understand_query(query: str) -> dict:
    llm = get_llm()

    prompt = f"""You are a Query Understanding Agent.

Analyze the query and return ONLY valid JSON with exactly these keys:

{{
    "intent": "<one sentence describing what the user wants>",
    "topics": ["<topic1>", "<topic2>"],
    "query_type": "<one of: research | comparison | summary | factual | general>"
}}

Rules:
- query_type MUST be one of: research, comparison, summary, factual, general
- Do not add any text outside the JSON

Query: {query}"""

    try:
        response = llm.invoke(prompt)
        result = _extract_json(response.content)

        # Validate and sanitize
        if not isinstance(result, dict):
            return _FALLBACK

        query_type = result.get("query_type", "general").lower().strip()
        if query_type not in _VALID_QUERY_TYPES:
            query_type = "general"

        return {
            "intent": str(result.get("intent", "")),
            "topics": result.get("topics", []) if isinstance(result.get("topics"), list) else [],
            "query_type": query_type,
        }
    except Exception:
        return _FALLBACK
