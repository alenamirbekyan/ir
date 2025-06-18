from method.sda import SDA
from method.metropolis_min_slot import metropolis
from summit import Graph, Node, shortest_path_tree
import json
from copy import deepcopy

def load_graph_by_name(filename, graph_name):
    with open(filename, "r") as f:
        data = json.load(f)

    for g in data["graphes"]:
        if g["name"] == graph_name:
            nodes = []
            for node in g["node"]:
                n = Node(level=node["level"], num=node["num"])
                n.parents = node["parents"]
                n.neighbors = node["neighbors"]
                n.childrens = node["childrens"]
                n.color = node["color"]
                nodes.append(n)
            return Graph(nodes, g["height"])
    return None

def compute_nb_slots(graph):
    root = graph.nodes[0]
    edges = shortest_path_tree(graph, root, [], [])
    planning = graph.resolution(edges, SDA())
    if isinstance(planning, dict) and planning:
        return max(planning.keys()) + 1
    return 0

# Charger le graphe 5000 nodes
graph = load_graph_by_name("save_file.json", "5000 nodes")

# SDA seul
graph_sda = deepcopy(graph)
sda_edges = shortest_path_tree(graph_sda, graph_sda.nodes[0], [], [])
graph_sda.resolution(sda_edges, SDA())
slots_sda = compute_nb_slots(graph_sda)

# SDA + Recuit (slots)
result = metropolis(deepcopy(graph))
slots_recuit = result["nb_slots"]

print("🎯 Résultat SDA vs SDA + Recuit (minimise nb_slots)")
print(f"SDA        : {slots_sda} slots")
print(f"SDA+Recuit : {slots_recuit} slots")
print(f"Gain       : {slots_sda - slots_recuit} slot(s)")
