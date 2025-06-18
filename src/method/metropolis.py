import random
import math
import time
from copy import deepcopy
from method.sda import SDA
from summit import shortest_path_tree


def compute_nb_slots(graph):
    root = graph.nodes[0]
    edges = shortest_path_tree(graph, root, [], [])
    planning = graph.resolution(edges, SDA())
    if isinstance(planning, dict) and planning:
        return max(slot for slot in planning) + 1
    return 0


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

    if alternatives:
        node.receiver = random.choice(alternatives)

    return neighbor


def metropolis(graph, initial_temp=100.0, cooling_rate=0.95, max_iterations=500):
    start_time = time.time()

    current_solution = generate_initial_solution(graph)
    best_solution = deepcopy(current_solution)

    current_cost = compute_nb_slots(current_solution)
    best_cost = current_cost
    T = initial_temp

    for iteration in range(max_iterations):
        neighbor = generate_neighbor(current_solution)
        neighbor_cost = compute_nb_slots(neighbor)
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

    elapsed_time = time.time() + start_time

    return {
        "best_graph": best_solution,
        "nb_slots": best_cost,
        "iterations": iteration + 1,
        "time": elapsed_time,
        "final_temp": T
    }

