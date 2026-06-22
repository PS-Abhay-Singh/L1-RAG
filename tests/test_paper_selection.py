from backend.app.agents.paper_selection_agent import (
    PaperSelectionAgent
)

papers = PaperSelectionAgent.select(
    "Compare HiRAG and LightRAG"
)

print(papers)
