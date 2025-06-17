from load_saved_graphs import load_graphs_from_file
from method.metropolis import metropolis
from method.experiments.runner_metropolis import run as run_batch

print("=== 🔬 Single Metropolis Test ===")
graphs = load_graphs_from_file("save_file.json")
g = graphs[1]  # Exemple : "10 nodes"

result = metropolis(g)

print(f"Tested: {g.name}")
print(f"Initial latency: {result['initial_latency']}")
print(f"Final latency: {result['latency']}")
print(f"Iterations: {result['iterations']}")
print(f"Execution time: {result['time']:.4f}s")
print(f"Final temperature: {result['final_temp']:.4f}")

print("\n=== 🧪 Batch Run on All Graphs ===")
run_batch()
