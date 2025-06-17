import json
from summit import Graph, Node

def load_graphs_from_file(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)

    graph_objects = []

    for graph_data in data["graphes"]:
        node_objects = []
        index_map = {}

        for raw_node in graph_data["node"]:
            node = Node(level=raw_node["level"], num=raw_node["num"])
            node.color = raw_node.get("color", "black")
            node_objects.append(node)
            index_map[node.num] = node 

        for raw_node in graph_data["node"]:
            node = index_map[raw_node["num"]]

            for pid in raw_node["parents"]:
                if pid in index_map:
                    node.add_parent(index_map[pid])

            for nid in raw_node["neighbors"]:
                if nid in index_map and nid not in node.neighbors:
                    node.add_neighbor(index_map[nid])


        graph = Graph(node_objects, graph_data["height"])
        graph.name = graph_data.get("name", "Unnamed")

        graph_objects.append(graph)

    return graph_objects
