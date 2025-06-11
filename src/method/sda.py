from method.method import Methode

class SDA(Methode):
    def solve(self, graph, shortest_path=[]):
        print("Starting SDA protocol")
        print("Initial shortest path tree:", shortest_path)

        # ─────────────────────────────────────────────
        # Step 1: Build parent/children relationships
        # ─────────────────────────────────────────────
        parent_of = {}       # child → parent
        children_of = {}     # parent → list of children
        all_nodes = set()
        children = set()
        solution = {}

        for parent, child in shortest_path:
            parent_of[child] = parent
            if parent not in children_of:
                children_of[parent] = []
            children_of[parent].append(child)
            all_nodes.update([parent, child])
            children.add(child)

        # ─────────────────────────────────────────────
        # Step 2: Identify the sink (the only node without parent)
        # ─────────────────────────────────────────────
        roots = list(all_nodes - children)
        if len(roots) != 1:
            print(f"Error: {len(roots)} roots detected instead of one.")
            return
        sink = roots[0]

        # ─────────────────────────────────────────────
        # Step 3: SDA scheduling process
        # ─────────────────────────────────────────────
        already_sent = set()          # nodes that already transmitted data
        slot = 1                      # current slot number
        max_idle_slots = 5            # safety to avoid infinite loops
        idle_slots = 0                # consecutive slots with no transmission

        while len(already_sent) < len(all_nodes) - 1:  # excluding the sink
            leaves = []

            # Identify ready leaves (whose children have already sent their data)
            for node in all_nodes:
                if node == sink or node in already_sent:
                    continue
                current_children = children_of.get(node, [])
                if all(child in already_sent for child in current_children):
                    leaves.append(node)

            # 🔽 Sort leaves by decreasing number of neighbors (more connected = more urgent)
            leaves.sort(key=lambda n: len(graph.sommets[n].get_voisins()), reverse=True)

            transmissions = []              # list of (sender, receiver)
            occupied_receivers = set()      # to avoid two children sending to the same parent

            # Choose transmissions for this slot
            for sender in leaves:
                receiver = parent_of.get(sender)
                if receiver is not None and receiver not in occupied_receivers:
                    transmissions.append((sender, receiver))
                    occupied_receivers.add(receiver)

            # Apply transmissions for the current slot
            if transmissions:
                for sender, receiver in transmissions:
                    already_sent.add(sender)
                    # graph.sommets[sender].color = "green"             # mark node as active
                    graph.sommets[sender].text = f"S{slot}"           # show slot in the node
                    graph.sommets[sender].destinataire = receiver     # for arrow drawing
                    graph.sommets[sender].textSiEnvoi = slot          # show slot on the edge
                    print(f"SLOT {slot}: {sender} sends to {receiver}")
                    if(slot in solution.keys()):
                        solution[slot].append((sender,receiver))
                    else:
                        solution[slot] = [(sender,receiver)]
                idle_slots = 0
            else:
                print(f"SLOT {slot}: no transmission possible. Stopping.")
                idle_slots += 1
                if idle_slots >= max_idle_slots:
                    print("Deadlock detected: too many idle slots.")
                    break

            slot += 1

        """# ─────────────────────────────────────────────
        # Step 4: Final coloring and reporting
        # ─────────────────────────────────────────────
        for node in graph.sommets:
            if node.num == sink:
                node.color = "red"
                print(f"Sink detected: {node.num}")
            elif node.num in already_sent:
                #node.color = "green"
            else:
                node.color = "black"
                print(f"Blocked or inactive node: {node.num}")"""

        print("SDA protocol completed.")
        return solution