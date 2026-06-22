from app.retrieval.fusion_retriever import FusionRetriever
from app.agents.citation_agent import CitationAgent

results = FusionRetriever.retrieve(
    "What is HiRAG?"
)

citations = CitationAgent.generate_sources(
    results
)

for citation in citations:
    print(citation)