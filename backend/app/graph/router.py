from backend.app.agents.query_understanding import understand_query


def route_query(state):
    result = understand_query(state["query"])
    state["task_type"] = result["query_type"]
    return state