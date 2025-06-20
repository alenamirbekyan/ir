import random
import math
import time
from copy import deepcopy
from export_json import save_graph
from method.sda import SDA
from summit import shortest_path_tree


def compute_nb_slots(graph):
    edges = [(node.receiver, node.num) for node in graph.nodes if node.receiver is not None]
    planning = graph.resolution(edges, SDA())
    if isinstance(planning, dict) and planning:
        return max(planning.keys()) + 1
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


def creates_cycle(graph, start, target):
    visited = set()
    stack = [target]
    while stack:
        node_id = stack.pop()
        if node_id == start:
            return True
        visited.add(node_id)
        for parent_id in graph.nodes[node_id].parents:
            if parent_id not in visited:
                stack.append(parent_id)
    return False


def mutate_graph_by_child_detour(graph):
    new_graph = deepcopy(graph)
    nodes = new_graph.nodes

    candidates = [
        n for n in nodes
        if n.num != 0 and n.childrens and n.parents and n.receiver is not None
    ]
    if not candidates:
        return None

    node = random.choice(candidates)
    old_parent_id = node.receiver
    old_parents = node.parents.copy()

    child_id = random.choice(node.childrens)
    child = nodes[child_id]

    possible_new_parents = [
        pid for pid in child.parents
        if pid != old_parent_id and pid != node.num and not creates_cycle(new_graph, node.num, pid)
    ]
    if not possible_new_parents:
        return None

    new_parent_id = random.choice(possible_new_parents)
    new_parent = nodes[new_parent_id]

    try:
        for pid in old_parents:
            if node.num in nodes[pid].childrens:
                nodes[pid].childrens.remove(node.num)

        node.parents = [new_parent_id]
        new_parent.childrens.append(node.num)
        node.receiver = new_parent_id

        return new_graph

    except Exception:
        return None


def metropolis(graph, initial_temp=100.0, cooling_rate=0.95, max_iterations=500,
               graph_name="unknown", method_name="metro", sda_nb_slots=None):
    start_time = time.time()

    current_solution = generate_initial_solution(graph)
    best_solution = deepcopy(current_solution)

    current_cost = compute_nb_slots(current_solution)
    best_cost = current_cost
    T = initial_temp

    for iteration in range(max_iterations):
        neighbor = mutate_graph_by_child_detour(current_solution)
        if neighbor is None:
            continue

        neighbor_cost = compute_nb_slots(neighbor)
        delta = neighbor_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / T):
            current_solution = neighbor
            current_cost = neighbor_cost

            if current_cost < best_cost:
                best_solution = deepcopy(neighbor)
                best_cost = current_cost

                # Sauvegarde uniquement si amélioration par rapport à SDA
                if sda_nb_slots is not None and best_cost < sda_nb_slots:
                    if sda_nb_slots is not None and best_cost < sda_nb_slots:
                        save_graph(
                            best_solution,
                            filename="saved_solutions",
                            slots=best_cost,
                            method=method_name,
                            graph_name=graph_name,
                            iteration=iteration
                        )


        T *= cooling_rate
        if T < 0.001:
            break

    return {
        "best_graph": best_solution,
        "nb_slots": best_cost,
        "iterations": iteration + 1,
        "time": time.time() - start_time,
        "final_temp": T
    }


def metropolis_2(graph, initial_temp=100.0, cooling_rate=0.98, max_iterations=500,
                 graph_name="unknown", method_name="metro2", sda_nb_slots=None):
    start_time = time.time()

    current_solution = generate_initial_solution(graph)
    best_solution = deepcopy(current_solution)

    current_cost = compute_nb_slots(current_solution)
    best_cost = current_cost
    T = initial_temp

    for iteration in range(max_iterations):
        neighbor = deepcopy(current_solution)

        nb_mutations = random.randint(3, 10)
        for _ in range(nb_mutations):
            mutated = mutate_graph_by_child_detour(neighbor)
            if mutated is None:
                break
            neighbor = mutated

        neighbor_cost = compute_nb_slots(neighbor)
        delta = neighbor_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / T):
            current_solution = neighbor
            current_cost = neighbor_cost

            if current_cost < best_cost:
                best_solution = deepcopy(neighbor)
                best_cost = current_cost

                # Sauvegarde uniquement si amélioration par rapport à SDA
                if sda_nb_slots is not None and best_cost < sda_nb_slots:
                    if sda_nb_slots is not None and best_cost < sda_nb_slots:
                        save_graph(
                            best_solution,
                            filename="saved_solutions",
                            slots=best_cost,
                            method=method_name,
                            graph_name=graph_name,
                            iteration=iteration
                        )


        T *= cooling_rate
        if T < 0.001:
            break

    return {
        "best_graph": best_solution,
        "nb_slots": best_cost,
        "iterations": iteration + 1,
        "time": time.time() - start_time,
        "final_temp": T
    }
