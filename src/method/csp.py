from method.method import Methode

class Csp(Methode):

    def solve(self, graph, recuit, shortest_paths=[]):

        niveau = {}

        for node in graph.nodes:
            niveau[node.num] = node.level

        sorted_nodes = dict(sorted(niveau.items(), key=lambda item: item[1], reverse = True))

        for key in sorted_nodes:
            pass
        return None