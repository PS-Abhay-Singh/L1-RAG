from langchain_core.prompts import ChatPromptTemplate
from ..llm import get_llm

llm = get_llm()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a comparative analysis agent. Compare the provided research papers across methodology, results, and conclusions. Return a structured JSON comparison."),
    ("human", "Query: {query}\n\nPapers:\n{papers}")
])

chain = prompt | llm

def compare_papers(query: str, papers: str) -> str:
    return chain.invoke({"query": query, "papers": papers}).content
