# test_filtered_retriever.py

from backend.app.retrieval.retriever import Retriever

results = Retriever.retrieve(
    query="HiRAG architecture",
    selected_papers=[
        "Retrieval-Augmented Generation with Hierarchical Knowledge"
    ]
)

for match in results.matches:

    print(
        match.metadata["paper_title"]
    )
