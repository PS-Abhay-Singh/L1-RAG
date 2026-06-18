from langchain_core.prompts import ChatPromptTemplate
from ..llm import get_llm

llm = get_llm()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research assistant. Rewrite the user query into 3 alternative search queries optimized for academic paper retrieval. Return as a JSON list."),
    ("human", "{query}")
])

chain = prompt | llm

def translate_query(query: str) -> str:
    return chain.invoke({"query": query}).content
