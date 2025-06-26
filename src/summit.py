import math
from random import randint, random
import random as rand

class Graph:
    def __init__(self, nodes, height):
        self.nodes = nodes  # List of all nodes in the graph
        self.min = {}       # Currently unused but could store min distances or other metadata
        self.height = height  # Number of levels in the hierarchical graph
        self.set_lower_bound()

    def load_graph(self, file, line):
        pass  # Placeholder for loading a graph from a file

    def save_graph(self, file):
        pass  # Placeholder for saving a graph to a file

    def count_nodes_in_level(self, level):
        """Return the number of nodes at a given level."""
        count = 0
        for node in self.nodes:
            if node.level == level:
                count += 1
        return count

    def resolution(self, shortest_path, method, recuit = None):
        """Apply the given method (SDA or Heuristic) on the graph."""
        return method.solve(self, recuit, shortest_path )

    def set_lower_bound(self):
        current_index = 0
        for i in range(self.height):
            while current_index < len(self.nodes) and self.nodes[current_index].level <= i:
                current_index += 1


    def toString(self):
        """Return a string representation of the graph in JSON-like format."""
        res = "{ \"height\":" + str(self.height) + ",\"node\":["
        first = True
        for node in self.nodes:
            if not first:
                res += ","
            first = False
            res += "{" + node.toString() + "}"
        return res + "]}\n"


class Node:
    def __init__(self, level, num):
        self.num = num                  # Unique identifier for the node
        self.level = level              # Vertical level (used for drawing)
        self.neighbors = []            # Undirected neighbors
        self.parents = []              # Parents (nodes at upper level connected to this one)
        self.childrens = []             # childrens (nodes at lower level connected from this one)
        self.color = "black"           # Used for visualization
        self.state = None              # Can hold any custom state
        self.text = ""                 # Label displayed in the node
        self.textOnSend = ""           # Text shown on the edge during data transmission
        self.receiver = None           # ID of the node that this node sends data to

    def get_neighbors(self):
        return self.neighbors

    def add_neighbor(self, node):
        """Add a bidirectional connection between two nodes."""
        if node.num not in self.neighbors:
            self.neighbors.append(node.num)
            node.neighbors.append(self.num)

    def remove_neighbor(self, node):
        if node.num in self.neighbors:
            self.neighbors.remove(node.num)
            node.remove_neighbor(self)

    def add_parent(self, parent):
        """Add a parent node and set this node as the child of that parent."""
        self.parents.append(parent.num)
        parent.add_child(self)

    def add_child(self, child):
        """Add a child node (used internally when assigning parents)."""
        self.childrens.append(child.num)

    def get_parents(self):
        return self.parents

    def get_childrens(self):
        return self.childrens

    def toString(self):
        """Return a JSON-like string representation of the node and its connections."""
        res = "\"num\":" + str(self.num) + ","
        res += "\"level\":" + str(self.level) + ","
        res += "\"color\":\"" + self.color + "\","

        res += "\"parents\":["
        res += ",".join(map(str, self.parents))
        res += "],"

        res += "\"neighbors\":["
        res += ",".join(map(str, self.neighbors))
        res += "],"

        res += "\"childrens\":["
        res += ",".join(map(str, self.childrens))
        res += "]"

        return res


def generate_graph(levels, max_nodes_per_level):
    """Generate a hierarchical graph with random connections between levels."""
    num = 0
    start_level = 0
    graph = []

    # Add the sink node (level 0)
    root = Node(0, num)
    root.color = "red"
    graph.append(root)

    for level in range(1, levels + 1):
        end_level = len(graph)
        node_count = randint(1, max_nodes_per_level)
        previous = None

        # Create nodes for the current level
        for _ in range(node_count):
            num += 1
            node = Node(level, num)
            graph.append(node)

            # Add horizontal random edge to previous node (within the same level)
            if previous is not None and randint(0, 2) == 2:
                node.add_neighbor(previous)

            previous = node

        # Create vertical connections (childrens ↔ parents)
        already_linked = []
        for i in range(end_level, end_level + node_count):
            current_node = graph[i]
            connection_count = randint(1, end_level - start_level)
            connection_count = min(connection_count, 3)

            for _ in range(connection_count):
                parent_candidate = graph[randint(start_level, end_level - 1)]
                if (current_node, parent_candidate) not in already_linked:
                    already_linked.append((current_node, parent_candidate))
                    current_node.add_parent(parent_candidate)

        # Prepare the range for the next level
        start_level = len(graph) - node_count

    return Graph(graph, levels)


def shortest_path_tree(graph, root_node, connection, used_childrens):
    """
    Build a shortest path tree rooted at the sink by traversing each child once.
    The output is a list of (parent, child) edges.
    """
    for child_id in root_node.get_childrens():
        if child_id not in used_childrens:
            connection.append((root_node.num, child_id))
            used_childrens.append(child_id)
            connection = shortest_path_tree(graph, graph.nodes[child_id], connection, used_childrens)
    return connection


def generate_scatter_plot(total_nodes, r):
    num = 0
    graph = []

    root = Node(0, num)

    graph.append(root)
    summit = {}
    summit[0] = (0,0)
    for i in range(1,total_nodes):
        # s = randint(0, i-1)
        s = i-1
        corner = rand.uniform(0, 2 * math.pi)
        radius = r * math.sqrt(rand.uniform(0.3, 1))  # sqrt pour une densité uniforme
        x2 = summit[s][0] + radius * math.cos(corner)
        y2 = summit[s][1] + radius * math.sin(corner)
        summit[i] = (x2,y2)
        node = Node(None, i)
        for n in range(i):
            x = summit[n][0]
            y = summit[n][1]
            if((x2 - x) ** 2 + (y2 - y) ** 2 <= r ** 2):
                node.add_neighbor(graph[n])
        graph.append(node)
    max_level = 0
    for n in graph:
        for v_ind in n.get_neighbors():
            v = graph[v_ind]
            if v.level is None or v.level > n.level+1:
                v.level = n.level+1
                if max_level < v.level:
                    max_level = v.level

    for n in graph:
        voisins = n.get_neighbors().copy()
        for v_ind in voisins:
            v = graph[v_ind]
            if v.level > n.level:
                v.add_parent(n)
                v.remove_neighbor(n)
    return (summit,Graph(graph, max_level))


def lose_time_summit(solution, graph):
    late = 0
    node = None
    res = None
    for k in solution.keys():
        for couple in solution[k]:
            tempo = k - (graph.height - graph.nodes[couple[0]].level) - late
            if (tempo) > late:
                late = tempo
                node = couple[0]
                res = couple
    # print((late, res))
    return (late, res)


def recuit_simule(solution, graph, max_solution, shortest_path, method):
    best_solution = solution
    best_max_solution = max_solution
    blocking_points = []
    if(max_solution > math.ceil(math.log2(len(graph.nodes))) and max_solution > graph.height):
        for i in range(500):
            info = lose_time_summit(solution, graph)
            if info[1] and not info[1] in blocking_points:
                blocking_points.append(info[1])
                new_solution = graph.resolution(shortest_path, method, blocking_points)
                if new_solution is None:
                    solution = {}
                    blocking_points.remove(info[1])
                else:
                    new_max_solution = max(new_solution.keys())+1
                    iteration = new_max_solution
                    delta = new_max_solution - max_solution
                    if delta<0:
                        best_solution = new_solution
                        best_max_solution = new_max_solution
                        solution = new_solution
                        max_solution = new_max_solution
                        if (max_solution == math.ceil(math.log2(len(graph.nodes))) or max_solution == graph.height):
                            print("meillieur apres calcul " + str(i))
                            return (best_solution, best_max_solution)
                    elif random() > 0.5:
                        solution = new_solution
                        max_solution = new_max_solution
                    else:
                        blocking_points.remove(info[1])
    else:
        print("pas d'ammelioration possible")
    return (best_solution, best_max_solution)