from app.agents.research_agent import (
    ResearchAgent
)

from app.agents.comparison_agent import (
    ComparisonAgent
)


def research_node(state):

    result = ResearchAgent.analyze(
        state["query"]
    )

    state["result"] = result

    return state


def comparison_node(state):

    result = ComparisonAgent.compare(
        state["query"]
    )

    state["result"] = result

    return state