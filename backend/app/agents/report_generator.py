from langchain_core.prompts import ChatPromptTemplate
from ..llm import get_llm

llm = get_llm()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research report writer. Synthesize the provided evidence, comparisons, and contradictions into a coherent, well-cited research summary. Use academic tone."),
    ("human", "Query: {query}\n\nEvidence:\n{evidence}\n\nComparisons:\n{comparisons}\n\nContradictions:\n{contradictions}")
])

chain = prompt | llm

def generate_report(query: str, evidence: str, comparisons: str, contradictions: str) -> str:
    return chain.invoke({
        "query": query,
        "evidence": evidence,
        "comparisons": comparisons,
        "contradictions": contradictions
    }).content
