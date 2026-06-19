from app.vectordb.pinecone_client import index


class VectorStore:

    @staticmethod
    def upsert_records(records):

        index.upsert(vectors=records)