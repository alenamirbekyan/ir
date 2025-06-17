import random
import math
import time
from copy import deepcopy
from method.sda import SDA
from summit import shortest_path_tree


def compute_latency(graph):
    latencies = [None] * len(graph.nodes)
    latencies[0] = 0  # sink

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

    return sum([l for l in latencies if l is not None])


def generate_initial_solution(graph):
    root = graph.nodes[0]
    shortest_path = shortest_path_tree(graph, root, [], [])
    _ = graph.resolution(shortest_path, SDA())

    solution = deepcopy(graph)
    for node in solution.nodes:
        node.receiver = None
    for parent_id, child_id in shortest_path:
        solution.nodes[child_id].receiver = parent_id

    return solution


def generate_neighbor(graph):
    neighbor = deepcopy(graph)
    candidates = [n for n in neighbor.nodes if n.num != 0 and len(n.parents) > 1]
    if not candidates:
        return neighbor

    node = random.choice(candidates)
    current_receiver = node.receiver
    alternatives = [p for p in node.parents if p != current_receiver]

    if not alternatives:
        return neighbor

    node.receiver = random.choice(alternatives)
    return neighbor


def metropolis(graph, initial_temp=100.0, cooling_rate=0.95, max_iterations=500):
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
