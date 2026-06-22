from backend.app.retrieval.retriever import Retriever

results = Retriever.retrieve(
    "What is HiRAG?"
)

for match in results.matches:

    print("=" * 60)

    print("SCORE:")
    print(match.score)

    print("\nSECTION:")
    print(match.metadata["section"])

    print("\nCONTENT:")
    print(match.metadata["content"][:300])
