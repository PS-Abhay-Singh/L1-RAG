from backend.app.retrieval.fusion_retriever import FusionRetriever

results = FusionRetriever.retrieve(
    "What is HiRAG?"
)

for idx, match in enumerate(results, start=1):

    print("=" * 60)

    print(f"RANK {idx}")

    print("SECTION:")
    print(match.metadata["section"])

    print()

    print("CONTENT:")
    print(match.metadata["content"][:250])
