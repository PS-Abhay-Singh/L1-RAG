from langchain_core.prompts import ChatPromptTemplate
from ..llm import get_llm

llm = get_llm()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a routing agent. Given a research query, decide which retrieval strategy to use: 'vector_search', 'keyword_search', or 'hybrid'. Return JSON with key 'strategy' and 'reason'."),
    ("human", "{query}")
])

chain = prompt | llm

def route_query(query: str) -> str:
    return chain.invoke({"query": query}).content
