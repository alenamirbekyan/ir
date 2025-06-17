from method.heuristic import Heuristic
from method.sda import SDA
from method.metropolis import metropolis, compute_latency
from load_saved_graphs import load_graphs_from_file
from summit import shortest_path_tree
from copy import deepcopy
import csv
import os
import time

def assign_receivers_from_edges(graph, edges):
    for n in graph.nodes:
        n.receiver = None
    for parent_id, child_id in edges:
        graph.nodes[child_id].receiver = parent_id
    return graph

def solve_with_method(graph, method_type):
    method = None
    if "SDA" in method_type:
        method = SDA()
    elif "Heuristic" in method_type:
        method = Heuristic()

    edges = shortest_path_tree(graph, graph.nodes[0], [], [])
    
    # ➕ Récupération du planning (slot) depuis la méthode
    planning = method.solve(graph, edges)

    if isinstance(planning, dict) and all(isinstance(k, int) for k in planning.keys()):
        nb_slots = max(planning.keys()) + 1 if planning else 0
    else:
        print(f"[WARN] Méthode {method_type} a retourné un planning non standard : {planning}")
        nb_slots = 0

    # ➕ Attribution des .receiver
    solution = graph.resolution(edges, method)
    solution = deepcopy(assign_receivers_from_edges(graph, edges))

    result = {
        "initial_latency": compute_latency(solution),
        "method": method_type,
        "nb_slots": nb_slots
    }

    if "+Recuit" in method_type:
        m_result = metropolis(solution)
        result.update({
            "final_latency": m_result["latency"],
            "iterations": m_result["iterations"],
            "execution_time": m_result["time"]
        })
    else:
        result.update({
            "final_latency": result["initial_latency"],
            "iterations": 0,
            "execution_time": 0.0
        })

    return result

def write_csv_line(file, graph, result):
    file_exists = os.path.exists(file)
    with open(file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["graph_name", "num_nodes", "height", "method",
                             "initial_latency", "final_latency",
                             "iterations", "execution_time", "nb_slots"])
        writer.writerow([
            graph.name,
            len(graph.nodes),
            graph.height,
            result["method"],
            result["initial_latency"],
            result["final_latency"],
            result["iterations"],
            round(result["execution_time"], 4),
            result["nb_slots"]
        ])

def run_all_methods():
    methods = ["SDA", "SDA+Recuit", "Heuristic", "Heuristic+Recuit"]
    graphs = load_graphs_from_file("save_file.json")
    output_path = "method/experiments/results/all_methods.csv"

    if os.path.exists(output_path):
        os.remove(output_path)

    for graph in graphs:
        for method_type in methods:
            result = solve_with_method(deepcopy(graph), method_type)
            write_csv_line(output_path, graph, result)
            print(f"{graph.name} - {method_type} : {result['final_latency']} slots={result['nb_slots']}")
