from ..llm import get_llm
import re

_SUMMARIZE_KEYWORDS = {"summarize", "summary", "overview", "brief", "outline", "tldr", "tl;dr", "what is this", "what does this"}

# Conversational filler that confuses small LLMs into thinking they need file access
_FILLER = re.compile(
    r"\b(can you|could you|please|this pdf|this document|this file|the pdf|the document|for me)\b",
    re.IGNORECASE
)


def _clean_query(query: str) -> str:
    return _FILLER.sub("", query).strip(" ,?!.")


def _is_summarization(query: str) -> bool:
    q = query.lower()
    return any(kw in q for kw in _SUMMARIZE_KEYWORDS)


def generate_answer(query: str, context: str):
    if not context or not context.strip():
        return "I could not find any relevant content in the uploaded documents to answer this question."

    llm = get_llm()
    clean_q = _clean_query(query)

    if _is_summarization(query):
        prompt = f"""You are a Document Assistant. Below is content extracted from a document.
Write a clear, structured summary of the content below.
Do NOT say you cannot access files. Do NOT ask for more input.
Just summarize the content provided.

CONTENT:
{context}

SUMMARY:"""
    else:
        prompt = f"""You are a Document Assistant.
Answer the question using ONLY the content provided below.
Do NOT say you cannot access files. Do NOT use outside knowledge.
If the answer is not in the content, say: "I could not find the answer in the provided document."

CONTENT:
{context}

QUESTION: {clean_q}
ANSWER:"""

    response = llm.invoke(prompt)
    return response.content