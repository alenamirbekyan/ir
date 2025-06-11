from method.method import Methode

class Heuristic(Methode):

    def solve(self, graph, shortest_paths=[]):
        print("Starting Heuristic Protocol")

        solution = {}
        send_order = []
        children_score = {}

        # Step 1: Compute a score for each node to guide priority
        for node in graph.sommets:
            # Weighted score: more children (×5), neighbors, and parents
            children_score[node.num] = (
                len(node.get_enfant()) * 5 +
                len(node.get_voisins()) +
                len(node.get_parent())
            )

        # Step 2: Sort nodes by increasing score (lowest priority first)
        sorted_nodes = dict(sorted(children_score.items(), key=lambda item: item[1]))

        sent = set()
        slot = 0

        # Step 3: Slot-based scheduling
        while len(sent) < len(graph.sommets) - 1:
            occupied_receivers = set()

            for node_id in sorted_nodes.keys():
                if node_id in sent or node_id in occupied_receivers:
                    continue

                children = graph.sommets[node_id].get_enfant()
                parents = graph.sommets[node_id].get_parent()

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
                        graph.sommets[node_id].textSiEnvoi = slot
                        graph.sommets[node_id].destinataire = p
                        sent.add(node_id)
                        occupied_receivers.add(p)

                        solution.setdefault(slot, []).append((node_id, p))
                        break
                else:
                    # Otherwise, try sending to any neighbor
                    for v in graph.sommets[node_id].get_voisins():
                        if v not in occupied_receivers and v not in sent:
                            graph.sommets[node_id].textSiEnvoi = slot
                            graph.sommets[node_id].destinataire = v
                            sent.add(node_id)
                            occupied_receivers.add(v)

                            solution.setdefault(slot, []).append((node_id, v))
                            break

            slot += 1

        print("Heuristic transmission plan:", solution)
        return solution
