import json
from copy import deepcopy
from method.sda import SDA
from method.metropolis import metropolis, metropolis_2, compute_nb_slots
from summit import Graph, Node, shortest_path_tree

def load_all_graphs(filename):
    """
    Charge tous les graphes depuis un fichier JSON.
    Retourne une liste de tuples : (nom, objet Graph).
    """
    with open(filename, "r") as f:
        data = json.load(f)

    graphs = []
    for g in data["graphes"]:
        nodes = []
        for node in g["node"]:
            n = Node(level=node["level"], num=node["num"])
            n.parents = node["parents"]
            n.neighbors = node["neighbors"]
            n.childrens = node["childrens"]
            n.color = node["color"]
            nodes.append(n)
        graphs.append((g["name"], Graph(nodes, g["height"])))
    return graphs

if __name__ == "__main__":
    graphs = load_all_graphs("save_file.json")

    print("\n=== Comparaison SDA vs Metropolis vs Metropolis2 ===\n")
    print(f"{'Graphe':<15} | {'SDA':<4} | {'Metro':<5} | {'Metro2':<6} | Gain1 | Gain2")

    for name, graph in graphs:
        # Étape 1 : SDA (base)
        graph_sda = deepcopy(graph)
        sda_edges = shortest_path_tree(graph_sda, graph_sda.nodes[0], [], [])
        graph_sda.resolution(sda_edges, SDA())
        slots_sda = compute_nb_slots(graph_sda)

        # Étape 2 : Metropolis simple
        result_metro = metropolis(deepcopy(graph), graph_name=name, method_name="metro", sda_nb_slots=slots_sda)
        slots_metro = result_metro["nb_slots"]

        # Étape 3 : Metropolis amélioré
        result_metro2 = metropolis_2(deepcopy(graph), graph_name=name, method_name="metro2", sda_nb_slots=slots_sda)
        slots_metro2 = result_metro2["nb_slots"]

        # Résultats
        gain1 = slots_sda - slots_metro
        gain2 = slots_sda - slots_metro2

        print(f"{name:<15} | {slots_sda:<4} | {slots_metro:<5} | {slots_metro2:<6} | {gain1:^5} | {gain2:^5}")
