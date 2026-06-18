from langchain_core.prompts import ChatPromptTemplate
from ..llm import get_llm

llm = get_llm()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a contradiction detection agent. Identify conflicting claims or findings across the provided research excerpts. Return JSON with key 'contradictions', each having 'claim_a', 'claim_b', 'source_a', 'source_b', and 'explanation'."),
    ("human", "Excerpts:\n{excerpts}")
])

chain = prompt | llm

def detect_contradictions(excerpts: str) -> str:
    return chain.invoke({"excerpts": excerpts}).content
