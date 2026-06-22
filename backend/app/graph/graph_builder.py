from langgraph.graph import (
    StateGraph,
    END
)

from app.graph.state import (
    GraphState
)

from app.graph.router import (
    route_query
)

from app.graph.nodes import (
    research_node,
    comparison_node
)


graph = StateGraph(GraphState)

graph.add_node(
    "router",
    route_query
)

graph.add_node(
    "research",
    research_node
)

graph.add_node(
    "comparison",
    comparison_node
)

def decide_route(state):

    if state["task_type"] == "comparison":

        return "comparison"

    return "research"

graph.set_entry_point(
    "router"
)

graph.add_conditional_edges(
    "router",
    decide_route,
    {
        "research": "research",
        "comparison": "comparison"
    }
)

graph.add_edge(
    "research",
    END
)

graph.add_edge(
    "comparison",
    END
)

research_graph = graph.compile()