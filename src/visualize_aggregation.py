import json
from copy import deepcopy
import matplotlib.pyplot as plt
import networkx as nx

from method.sda import SDA
from method.metropolis import metropolis
from summit import Graph, Node


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


def apply_sda(graph):
    root = graph.nodes[0]
    edges = []
    visited = set()

    def dfs(n):
        for child_id in n.get_childrens():
            if child_id not in visited:
                visited.add(child_id)
                edges.append((n.num, child_id))
                dfs(graph.nodes[child_id])

    dfs(root)
    graph.resolution(edges, SDA())
    for parent_id, child_id in edges:
        graph.nodes[child_id].receiver = parent_id

    return deepcopy(graph)


def extract_edges(graph):
    return [(n.receiver, n.num) for n in graph.nodes if n.receiver is not None]


def draw_graph(graph, ax, title):
    G = nx.DiGraph()
    G.add_nodes_from([n.num for n in graph.nodes])
    G.add_edges_from(extract_edges(graph))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, ax=ax, with_labels=True, arrows=True, node_size=500, node_color="lightblue")
    ax.set_title(title)


# Charger et traiter le graphe à 50 sommets
original_graph = load_graph_by_name("save_file.json", "50 nodes")
sda_graph = apply_sda(deepcopy(original_graph))
recuit_result = metropolis(deepcopy(sda_graph))
recuit_graph = recuit_result["best_graph"]

# Affichage des 2 arbres
fig, axs = plt.subplots(1, 2, figsize=(14, 7))
draw_graph(sda_graph, axs[0], "SDA - Avant Recuit")
draw_graph(recuit_graph, axs[1], "SDA - Après Recuit")
plt.tight_layout()
plt.show()
