# test_delete.py

from backend.app.vectordb.pinecone_client import index

index.delete(delete_all=True)

print("Deleted")
