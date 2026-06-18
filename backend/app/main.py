from app.agents.query_understanding import understand_query


query = "Compare GraphRAG and Agentic RAG"

result = understand_query(query)

print(result)