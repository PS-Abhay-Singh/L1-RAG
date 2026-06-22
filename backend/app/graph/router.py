import json

from app.agents.query_understanding import (
    understand_query
)


def route_query(state):

    query = state["query"]

    result = understand_query(query)

    if isinstance(result, str):
        result = json.loads(result)

    state["task_type"] = result[
        "query_type"
    ]

    return state