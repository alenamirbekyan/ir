from random import randint
from method.method import Methode
from collections import defaultdict

class Csp(Methode):

    def solve(self, graph, recuit, shortest_paths=[]):
        niveau = {}

        for node in graph.nodes:
            niveau[node.num] = node.level

        sorted_nodes = dict(sorted(niveau.items(), key=lambda item: item[1], reverse=True))

        solution = {}

        for node in sorted_nodes:
            if node != 0:
                slot = graph.height - graph.nodes[node].level
                parents = graph.nodes[node].get_parents()
                random_parent = parents[randint(0, len(parents) - 1)]
                solution.setdefault(slot, []).append((node, random_parent))

        print("[CSP] Solution initiale :", solution)

        solution = self.reparer_collisions(solution)
        solution = self.reparer_precedence(solution, graph)
        solution = self.reparer_chevauchement(solution)  # ⬅️ ajout ici
        return solution

    def reparer_collisions(self, solution):
        print("\n[CSP] Correction des collisions")
        new_solution = defaultdict(list)
        used = defaultdict(set)

        for slot in sorted(solution.keys()):
            for node, parent in solution[slot]:
                s = slot
                while parent in used[s]:
                    s += 1
                new_solution[s].append((node, parent))
                used[s].add(parent)
                print(f"  ➤ Node {node} → Parent {parent} assigné au slot {s}")

        return dict(new_solution)

    def count_precedence_violations(self, solution, node, graph):
        slot_u = self.find_slot(solution, node)
        violations = 0
        for child in graph.nodes[node].childrens:
            child_slot = self.find_slot(solution, child)
            if child_slot is not None and child_slot >= slot_u:
                violations += 1
        return violations

    def find_slot(self, solution, node_num):
        for slot, transmissions in solution.items():
            for node, _ in transmissions:
                if node == node_num:
                    return slot
        return None

    def reparer_precedence(self, solution, graph):
        print("\n[CSP] Correction des précédences")
        modified = True

        while modified:
            modified = False
            all_nodes = set(n for transmissions in solution.values() for n, _ in transmissions)
            violations = []

            for node_num in all_nodes:
                count = self.count_precedence_violations(solution, node_num, graph)
                if count > 0:
                    violations.append((node_num, count))

            violations.sort(key=lambda x: x[1], reverse=True)

            for node_num, _ in violations:
                current_slot = self.find_slot(solution, node_num)
                transmission = None

                for (n, p) in solution[current_slot]:
                    if n == node_num:
                        transmission = (n, p)
                        break
                if transmission:
                    solution[current_slot].remove(transmission)
                    new_slot = current_slot + 1
                    print(f"  🔁 Node {node_num} déplacé de slot {current_slot} à {new_slot} (précédence)")
                    while any(p == transmission[1] for (n, p) in solution.get(new_slot, [])):
                        new_slot += 1
                    solution.setdefault(new_slot, []).append(transmission)
                    modified = True
                    break

        return solution

    def reparer_chevauchement(self, solution):
        print("\n[CSP] Correction des chevauchements")
        new_solution = defaultdict(list)
        used = defaultdict(lambda: defaultdict(list))  # used[slot][parent] = [nodes]

        for slot in sorted(solution.keys()):
            for node, parent in solution[slot]:
                s = slot
                while len(used[s][parent]) >= 1:
                    s += 1
                new_solution[s].append((node, parent))
                used[s][parent].append(node)
                print(f"  ↪️ Node {node} → Parent {parent} assigné au slot {s} (chevauchement évité)")

        return dict(new_solution)
