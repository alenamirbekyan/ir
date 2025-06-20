import json
import os

def save_graph(graph, filename, slots, method="metro", graph_name="unknown", iteration=0):
    data = {
        "name": f"{graph_name}_{method}_slots{slots}_iter{iteration}",
        "height": graph.height,
        "node": []
    }
    for node in graph.nodes:
        data["node"].append({
            "num": node.num,
            "level": node.level,
            "parents": node.parents,
            "neighbors": node.neighbors,
            "childrens": node.childrens,
            "color": node.color,
            "receiver": node.receiver
        })

    os.makedirs("saved_solutions", exist_ok=True)
    with open(f"saved_solutions/{data['name']}.json", "w") as f:
        json.dump(data, f, indent=2)
