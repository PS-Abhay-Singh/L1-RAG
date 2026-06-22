from backend.app.graph.graph_builder import (
    research_graph
)

result = research_graph.invoke(
    {
        "query":
        "Compare HiRAG and LightRAG",

        "task_type": "",

        "result": ""
    }
)

print(result["result"])
