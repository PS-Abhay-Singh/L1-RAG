from backend.app.retrieval.multi_query_retriever import MultiQueryRetriever
from backend.app.retrieval.rrf import RRF


class FusionRetriever:

    @staticmethod
    def retrieve(query: str):

        multi_results = MultiQueryRetriever.retrieve(
            query
        )

        fused_results = RRF.fuse(
            multi_results
        )

        return fused_results[:5]