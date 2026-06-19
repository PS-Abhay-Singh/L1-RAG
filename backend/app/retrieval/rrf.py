from collections import defaultdict


class RRF:

    @staticmethod
    def fuse(results_list, k=60):

        scores = defaultdict(float)
        documents = {}

        for results in results_list:

            for rank, match in enumerate(results.matches):

                doc_id = match.id

                rrf_score = 1 / (k + rank + 1)

                scores[doc_id] += rrf_score

                documents[doc_id] = match

        ranked_docs = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            documents[doc_id]
            for doc_id, _ in ranked_docs
        ]