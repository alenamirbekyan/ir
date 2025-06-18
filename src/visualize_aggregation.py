
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
    planning = graph.resolution(edges, SDA())
    for parent_id, child_id in edges:
        graph.nodes[child_id].receiver = parent_id

    return deepcopy(graph), planning


def extract_edges(graph):
    return [(n.num, n.receiver) for n in graph.nodes if n.receiver is not None]


def hierarchy_pos(graph):
    levels = {}
    for node in graph.nodes:
        level = node.level
        if level not in levels:
            levels[level] = []
        levels[level].append(node.num)

    pos = {}
    max_width = max(len(nodes) for nodes in levels.values())
    for lvl, nodes in levels.items():
        for i, node in enumerate(nodes):
            x = i / (len(nodes) - 1) if len(nodes) > 1 else 0.5
            y = -lvl
            pos[node] = (x, y)
    return pos


def build_edge_labels(planning, graph):
    edge_labels = {}
    if not isinstance(planning, dict):
        return edge_labels
    for slot, transmissions in planning.items():
        for (src, dst) in transmissions:
            edge_labels[(dst, src)] = f"S{slot}"  # affichage inversé (flèche enfant → parent)
    return edge_labels


def draw_graph(graph, planning, ax, title, pos):
    G = nx.DiGraph()
    G.add_nodes_from([n.num for n in graph.nodes])
    G.add_edges_from(extract_edges(graph))
    edge_labels = build_edge_labels(planning, graph)
    nx.draw(G, pos, ax=ax, with_labels=True, arrows=True, node_size=500, node_color="lightblue")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="black", ax=ax)
    ax.set_title(title)


# Charger le graphe
original_graph = load_graph_by_name("save_file.json", "50 nodes")

# SDA
sda_graph, sda_planning = apply_sda(deepcopy(original_graph))

# Recuit
recuit_result = metropolis(deepcopy(sda_graph))
recuit_graph = recuit_result["best_graph"]
recuit_planning = None  # Le recuit n'a pas de slots attribués explicitement ici

# Positions hiérarchiques
shared_pos = hierarchy_pos(sda_graph)

# Affichage
fig, axs = plt.subplots(1, 2, figsize=(16, 8))
draw_graph(sda_graph, sda_planning, axs[0], "SDA - Avant Recuit", shared_pos)
draw_graph(recuit_graph, recuit_planning, axs[1], "SDA - Après Recuit", shared_pos)
plt.tight_layout()
plt.show()

