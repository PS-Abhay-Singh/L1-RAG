from langchain_core.prompts import ChatPromptTemplate
from backend.app.llm import get_llm

llm = get_llm()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research analyst. Extract key claims, findings, and supporting evidence from the provided paper excerpt. Return as JSON with keys: 'claims', 'findings', 'evidence'."),
    ("human", "Query: {query}\n\nPaper excerpt:\n{context}")
])

chain = prompt | llm

def extract_evidence(query: str, context: str) -> str:
    return chain.invoke({"query": query, "context": context}).content
