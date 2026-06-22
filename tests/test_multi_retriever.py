from backend.app.retrieval.multi_query_retriever import MultiQueryRetriever

results = MultiQueryRetriever.retrieve(
    "What is HiRAG?"
)

for i, query_results in enumerate(results):

    print("=" * 80)

    print(f"QUERY {i+1}")

    for match in query_results.matches[:2]:

        print(
            match.metadata["section"]
        )
