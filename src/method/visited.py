from method.method import Methode

class Visited(Methode):

    def solve(self, graph, recuit, shortest_paths=[]):
        solution = {}
        niv = graph.height
        sent = []
        sent_by_slot = {}
        while niv > 0:
            children_score = {}
            for node in graph.nodes:
                if(node.level == niv):
                    children_score[node.num] = (
                            len(list(set(node.get_neighbors()) - set(sent)))+
                            len(list(set(node.get_parents()) - set(sent)))
                    )

            sorted_nodes = dict(sorted(children_score.items(), key=lambda item: item[1]))
            for n_id in sorted_nodes:
                n = graph.nodes[n_id]
                slot = 0
                trouver = False
                while not trouver:
                    occuper = False
                    for key in solution.keys():
                        for couple in solution[key]:
                            if couple[1] == n_id and slot <= key:
                                occuper = True
                                slot = key
                    # if not occuper:
                    #     children = n.get_childrens()
                    #     for child in children:
                    #         if (n_id, child) in shortest_paths:
                    #             a_envoyer = False
                    #             for i in range(slot):
                    #                 if (i in sent_by_slot.keys()):
                    #                     liste = sent_by_slot[i]
                    #                     if child in liste:
                    #                         a_envoyer = True
                    #             if not a_envoyer:
                    #                 occuper = True


                    if not occuper:
                        possible = list(set(n.get_neighbors() + n.get_parents()) - set(sent))
                        for v_possible in possible:
                            peut_envoyer = True
                            if(slot in solution.keys()):
                                for couple in solution[slot]:
                                    if couple[1] == v_possible:
                                        peut_envoyer = False
                                        break
                            if peut_envoyer:
                                trouver = True
                                sent.append(n_id)
                                sent_by_slot.setdefault(slot, []).append(n_id)
                                solution.setdefault(slot, []).append((n_id, v_possible))
                                n.textOnSend = slot
                                n.receiver = v_possible
                                break
                    slot+=1
            niv-=1
        return solution