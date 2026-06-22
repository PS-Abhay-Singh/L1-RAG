from backend.app.vectordb.pinecone_client import index

stats = index.describe_index_stats()

print(stats)
