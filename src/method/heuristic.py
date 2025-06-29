from random import randint

from method.method import Methode

class Heuristic(Methode):

    def solve(self, graph, recuit, shortest_paths=[]):

        solution = {}
        children_score = {}

        # Step 1: Compute a score for each node to guide priority

        sent = set()
        slot = 0
        occupied_receivers = set()

        first = False

        if recuit and len(recuit) > 0:
            solution[0] = []
            for improvement in recuit:
                node = graph.nodes[improvement[0]]
                possible_node = node.get_childrens() + node.get_neighbors() + node.get_parents()
                possible_node.remove(improvement[1])
                elem_to_remove = []
                for n_id in possible_node:
                    n = graph.nodes[n_id]
                    if len(n.get_childrens() + n.get_neighbors() + n.get_parents()) == 1:
                        elem_to_remove.append(n_id)
                    elif n_id in sent or n_id in occupied_receivers:
                        elem_to_remove.append(n_id)
                possible_node = list(set(possible_node) - set(elem_to_remove))
                if(len(possible_node) == 0):
                    return None
                random_node = possible_node[randint(0, len(possible_node)-1)]
                solution[0].append((improvement[0], random_node))
                sent.add(improvement[0])
                occupied_receivers.add(improvement[0])
                occupied_receivers.add(random_node)
                graph.nodes[improvement[0]].textOnSend = 0
                graph.nodes[improvement[0]].receiver = random_node
                first = True

        for node in graph.nodes:
            # Weighted score: more children (×5), neighbors, and parents
            children_score[node.num] = (
                len(list(set(node.get_childrens()) - set(occupied_receivers))) * 5 +
                len(node.get_neighbors()) +
                len(node.get_parents())
            )


        # Step 2: Sort nodes by increasing score (lowest priority first)
        sorted_nodes = dict(sorted(children_score.items(), key=lambda item: item[1]))

        # Step 3: Slot-based scheduling
        iteration = 0
        while len(sent) < len(graph.nodes) - 1 and iteration < 1000:
            iteration+=1
            if(not (recuit and first)):
                occupied_receivers = set()
            else:
                first = False

            for node_id in sorted_nodes.keys():
                if node_id in sent or node_id in occupied_receivers:
                    continue

                children = graph.nodes[node_id].get_childrens()
                parents = graph.nodes[node_id].get_parents()

                # A node can send only if all its children already sent
                can_send = True
                for child in children:
                    if child not in sent and (node_id, child) in shortest_paths:
                        can_send = False

                if not can_send:
                    continue

                # Try sending to a parent
                for p in parents:
                    if p not in sent and p not in occupied_receivers:
                        graph.nodes[node_id].textOnSend = slot
                        graph.nodes[node_id].receiver = p
                        sent.add(node_id)
                        occupied_receivers.add(p)

                        solution.setdefault(slot, []).append((node_id, p))
                        break
                else:
                    # Otherwise, try sending to any neighbor
                    for v in graph.nodes[node_id].get_neighbors():
                        if v not in occupied_receivers and v not in sent:
                            graph.nodes[node_id].textOnSend = slot
                            graph.nodes[node_id].receiver = v
                            sent.add(node_id)
                            occupied_receivers.add(v)

                            solution.setdefault(slot, []).append((node_id, v))
                            break

            slot += 1

        # print(solution)
        if iteration == 1000:
            return None
        return solution
