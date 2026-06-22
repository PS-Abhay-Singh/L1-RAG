from backend.app.vectordb.pinecone_client import index


class VectorStore:

    @staticmethod
    def upsert_records(records):

        index.upsert(vectors=records)

    @staticmethod
    def delete_by_source_file(source_file: str):
        if not source_file:
            return

        index.delete(filter={"source_file": source_file})

    @staticmethod
    def delete_all():
        index.delete(delete_all=True)