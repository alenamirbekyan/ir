import os
import csv
from load_saved_graphs import load_graphs_from_file
from method.metropolis import metropolis

SAVE_PATH = "method/experiments/results"

def ensure_results_dir():
    os.makedirs(SAVE_PATH, exist_ok=True)

def extract_graph_size(graph):
    return len(graph.nodes)

def save_result_to_csv(graph, result):
    size = extract_graph_size(graph)
    filename = f"{SAVE_PATH}/results_{size}.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "graph_name", "num_nodes", "height",
                "initial_latency", "final_latency",
                "iterations", "execution_time", "final_temp"
            ])

        writer.writerow([
            getattr(graph, "name", "Unnamed"),
            len(graph.nodes),
            graph.height,
            result["initial_latency"],
            result["latency"],
            result["iterations"],
            round(result["time"], 4),
            round(result["final_temp"], 4)
        ])

def run():
    ensure_results_dir()
    graphs = load_graphs_from_file("save_file.json")
    print(f"🔍 Running Metropolis on {len(graphs)} graphs...")

    for i, graph in enumerate(graphs):
        print(f"→ {i+1}/{len(graphs)} | {graph.name} ({len(graph.nodes)} nodes)")

        result = metropolis(graph)
        save_result_to_csv(graph, result)

    print("✅ All results saved to:", SAVE_PATH)

if __name__ == "__main__":
    run()
