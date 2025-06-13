from math import trunc
from random import randint


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
            elif node.level > level:
                return count
        return count

    def resolution(self, shortest_path, method):
        """Apply the given method (SDA or Heuristic) on the graph."""
        return method.solve(self, shortest_path)

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

def generate_graph_by_nodes(total_nodes):
    """
    Generate a hierarchical graph with a fixed number of nodes (including sink at level 0).
    The levels and node distributions are randomly chosen.
    Ensures that every level up to the last has at least one node.
    """
    if total_nodes < 1:
        raise ValueError("Total nodes must be at least 1.")

    num = 0
    graph = []

    # Sink node at level 0
    root = Node(0, num)
    root.color = "red"
    graph.append(root)

    num += 1
    current_level = 1

    while num < total_nodes:
        nodes_this_level = min(randint(1, 5), total_nodes - num)
        start_index = len(graph)

        previous = None
        for _ in range(nodes_this_level):
            node = Node(current_level, num)
            graph.append(node)
            if previous and randint(0, 2) == 2:
                node.add_neighbor(previous)
            previous = node
            num += 1

        for i in range(start_index, len(graph)):
            current_node = graph[i]
            parent_count = randint(1, min(3, start_index))
            linked = set()
            for _ in range(parent_count):
                parent = graph[randint(0, start_index - 1)]
                if parent.num not in linked:
                    current_node.add_parent(parent)
                    linked.add(parent.num)

        current_level += 1

    # ─────────────────────────────────────
    # Ensure that all levels exist (safety)
    # ─────────────────────────────────────
    used_levels = {node.level for node in graph}
    for lvl in range(current_level):
        if lvl not in used_levels:
            num += 1
            missing = Node(lvl, num)
            graph.append(missing)
    graph.sort(key=lambda node: node.level)  
    return Graph(graph, current_level)
