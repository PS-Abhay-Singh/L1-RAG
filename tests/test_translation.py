# test_translation.py
from backend.app.agents.query_translation import translate_query

queries = translate_query(
    "What is HiRAG?"
)

print(type(queries))
print(queries)
