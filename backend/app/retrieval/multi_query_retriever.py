from app.retrieval.retriever import Retriever
from app.agents.query_translation import translate_query


class MultiQueryRetriever:

    @staticmethod
    def retrieve(query: str):

        translated_queries = translate_query(query)

        all_results = []

        for q in translated_queries:

            results = Retriever.retrieve(
                q,
                top_k=5
            )

            all_results.append(results)

        return all_results