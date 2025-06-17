import random
import math
import time
from copy import deepcopy
from method.heuristic import Heuristic
from method.sda import SDA
from summit import generate_graph, shortest_path_tree, generate_scatter_plot


def compute_latency(graph):
    """
    Compute the total latency (sum of distances from each node to sink).
    Assumes sink is node 0 and each node knows its receiver.
    """
    latencies = [None] * len(graph.nodes)
    latencies[0] = 0  # sink has zero latency

    changed = True
    while changed:
        changed = False
        for node in graph.nodes:
            if node.num == 0:
                continue
            parent_id = node.receiver
            if parent_id is not None and latencies[parent_id] is not None:
                new_latency = latencies[parent_id] + 1
                if latencies[node.num] is None or latencies[node.num] > new_latency:
                    latencies[node.num] = new_latency
                    changed = True

    total = sum([l for l in latencies if l is not None])
    return total


def generate_initial_solution(graph):
    """
    Build a spanning tree using the existing children structure.
    Assigns each node a receiver (who it sends data to).
    """
    shortest_path = shortest_path_tree(graph, graph.nodes[0], [], [])
    solution = graph.resolution(shortest_path, SDA())
    return deepcopy(solution)


def generate_neighbor(graph):
    """
    Generate a neighbor by changing one node's receiver among its parents.
    """
    neighbor = deepcopy(graph)
    candidates = [n for n in neighbor.nodes if len(n.parents) > 0 and n.num != 0]
    if not candidates:
        return neighbor

    node = random.choice(candidates)
    new_parent = random.choice(node.parents)
    node.receiver = new_parent
    return neighbor


def metropolis(graph, initial_temp=100.0, cooling_rate=0.95, max_iterations=500):
    """
    Metropolis algorithm for latency minimization
    """
    start_time = time.time()

    current_solution = generate_initial_solution(graph)
    best_solution = deepcopy(current_solution)

    current_cost = compute_latency(current_solution)
    best_cost = current_cost

    T = initial_temp

    for iteration in range(max_iterations):
        neighbor = generate_neighbor(current_solution)
        neighbor_cost = compute_latency(neighbor)

        delta = neighbor_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / T):
            current_solution = neighbor
            current_cost = neighbor_cost

            if current_cost < best_cost:
                best_solution = deepcopy(current_solution)
                best_cost = current_cost

        T *= cooling_rate
        if T < 0.001:
            break

    elapsed_time = time.time() - start_time

    return {
        "best_graph": best_solution,
        "latency": best_cost,
        "initial_latency": compute_latency(generate_initial_solution(graph)),
        "iterations": iteration + 1,
        "time": elapsed_time,
        "final_temp": T
    }
