from langchain_core.prompts import ChatPromptTemplate
from ..llm import get_llm

llm = get_llm()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a citation verification agent. Given a claim and its cited source excerpt, determine if the source actually supports the claim. Return JSON with keys: 'supported' (bool), 'confidence' (0-1), 'explanation'."),
    ("human", "Claim: {claim}\n\nSource excerpt:\n{source}")
])

chain = prompt | llm

def verify_citation(claim: str, source: str) -> str:
    return chain.invoke({"claim": claim, "source": source}).content
