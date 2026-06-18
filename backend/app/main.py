from backend.app.agents import understand_query
from backend.app.agents import translate_query


query = "Compare GraphRAG and Agentic RAG"

print("===== QUERY UNDERSTANDING =====")
print(understand_query(query))

print("\n===== QUERY TRANSLATION =====")
print(translate_query(query))