from method.method import Methode

class Heuristic(Methode):

    def solve(self, graph, shortest_paths=[]):
        print("Starting Heuristic Protocol")

        solution = {}
        children_score = {}

        # Step 1: Compute a score for each node to guide priority
        for node in graph.nodes:
            # Weighted score: more children (×5), neighbors, and parents
            children_score[node.num] = (
                len(node.get_childrens()) * 5 +
                len(node.get_neighbors()) +
                len(node.get_parents())
            )

        # Step 2: Sort nodes by increasing score (lowest priority first)
        sorted_nodes = dict(sorted(children_score.items(), key=lambda item: item[1]))

        sent = set()
        slot = 0

        # Step 3: Slot-based scheduling
        while len(sent) < len(graph.nodes) - 1:
            occupied_receivers = set()

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

        print("Heuristic transmission plan:", solution)
        return solution
