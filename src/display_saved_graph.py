import json
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph_from_json(path):
    with open(path, 'r') as f:
        data = json.load(f)

    G = nx.DiGraph()
    pos = {}
    labels = {}

    nodes = data['node']
    height = data['height']

    # Crée les nœuds avec leurs niveaux
    for node in nodes:
        num = node['num']
        level = node['level']
        pos[num] = (level, -num)  # Position simple
        labels[num] = str(num)
        G.add_node(num, color=node['color'])

    # Ajoute les arêtes : du noeud vers son receiver (vers la racine)
    for node in nodes:
        if node['receiver'] is not None:
            G.add_edge(node['num'], node['receiver'])  # ← ICI le sens est inversé

    # Coloration
    colors = ['red' if G.nodes[n]['color'] == 'red' else 'green' for n in G.nodes]

    # Dessin
    plt.figure(figsize=(8, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        labels=labels,
        node_color=colors,
        node_size=700,
        font_weight='bold',
        edge_color='black',
        arrows=True,
        arrowstyle='-|>',
        arrowsize=20
    )

    plt.title(f"{data['name']} (height={height})")
    plt.axis('off')
    plt.tight_layout()
    plt.show()


# === Exemple d’appel ===
if __name__ == "__main__":
    draw_graph_from_json("saved_solutions/exemple_metro_slots4_iter0.json")
