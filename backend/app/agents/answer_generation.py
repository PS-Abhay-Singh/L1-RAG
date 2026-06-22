from ..llm import get_llm


def generate_answer(
    query: str,
    context: str
):

    llm = get_llm()

    prompt = f"""
You are a Research Assistant.

Answer ONLY using the provided context.

If the answer is not present in the context,
say:

"I could not find the answer in the paper."

CONTEXT:

{context}

QUESTION:

{query}
"""

    response = llm.invoke(prompt)

    return response.content