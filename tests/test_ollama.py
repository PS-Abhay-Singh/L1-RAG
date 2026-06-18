from backend.app.agents import understand_query


query = "Compare GraphRAG and Agentic RAG"

result = understand_query(query)

print(result)
