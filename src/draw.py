import math
import turtle as turtle
import tkinter as TK

from method.heuristic import Heuristic
from method.sda import SDA
from save import *
from summit import generate_graph, shortest_path_tree

# Valeurs par défaut
size = 5
per_level = 5
method = Heuristic()

root = TK.Tk()
root.title("Sensor Protocol Visualizer")

# Canvas & Turtle
canvas = turtle.ScrolledCanvas(root, width=1280, height=700)
screen = turtle.TurtleScreen(canvas)
screen.screensize(1280, size * 80 + 300)
pen = turtle.RawTurtle(screen)
pen.hideturtle()
pen.speed(0)
screen.tracer(0, 0)

graph = None
coordinates = {}
solution = {}
iteration = 0

# Dropdown 
method_var = TK.StringVar(root)
method_var.set("Heuristic")

def update_method(*args):
    global method
    selected = method_var.get()
    if selected == "Heuristic":
        method = Heuristic()
    elif selected == "SDA":
        method = SDA()
    if graph:
        generate(True)

method_var.trace_add("write", lambda *args: update_method())
method_menu = TK.OptionMenu(root, method_var, "Heuristic", "SDA")

# Entrées utilisateur pour `size` et `per_level`
size_entry = TK.Entry(root, width=5)
size_entry.insert(0, "5")
per_level_entry = TK.Entry(root, width=5)
per_level_entry.insert(0, "5")

def lighten_color(color_name, factor=0.5):
    rgb_16bit = root.winfo_rgb(color_name)
    rgb_8bit = [int(c / 65535 * 255) for c in rgb_16bit]
    light_rgb = [int(c + (255 - c) * factor) for c in rgb_8bit]
    return '#%02x%02x%02x' % tuple(light_rgb)

def draw_node(node, color):
    pen.teleport(coordinates[node.num][0] - 10, coordinates[node.num][1] - 16.8)
    pen.color(color)
    pen.setheading(0)
    pen.fillcolor(lighten_color(color))
    pen.begin_fill()
    for _ in range(6):
        pen.forward(20)
        pen.left(60)
    pen.end_fill()
    pen.fillcolor(color)
    pen.teleport(coordinates[node.num][0], coordinates[node.num][1])
    pen.write(node.num, align="center")

def draw_edge(node1, node2, label, color="black"):
    x1, y1 = coordinates[node1.num]
    x2, y2 = coordinates[node2.num]

    pen.teleport(x1, y1)
    pen.color(color)
    pen.goto(x2, y2)

    if label != "":
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        offset = 25
        pen.teleport(x1 + math.cos(math.radians(angle)) * offset,
                     y1 + math.sin(math.radians(angle)) * offset)
        pen.write(label, align="center")

def generate(from_load=False):
    global graph, solution, iteration, size, per_level

    # Récupère les valeurs depuis les champs
    try:
        size = int(size_entry.get())
        per_level = int(per_level_entry.get())
        screen.screensize(1280, size * 80 + 300)
    except ValueError:
        print("Les valeurs de taille doivent être des entiers.")
        return

    if not from_load:
        graph = generate_graph(size, per_level)

    shortest_path = shortest_path_tree(graph, graph.nodes[0], [], [])
    if not shortest_path:
        print("Le plus court chemin est vide. Le graphe est probablement mal formé.")
        solution = {}
        return

    solution = graph.resolution(shortest_path, method)
    if solution is None:
        print("Aucun plan de transmission trouvé.")
        solution = {}

    iteration = -1
    draw()

def draw_max_slot_label(slot):
    """Display the total number of slots used in the solution at a fixed position."""
    pen.color("black")
    pen.teleport(-600,size * 40)  
    pen.write(f"Total slots: {slot + 1}", align="left", font=("Arial", 12, "bold"))



def draw():
    global iteration, coordinates

    canvas.delete("all")
    visited_edges = []
    coordinates = {}
    current_level = math.inf
    nodes_at_level = 0
    index = 0

    pen.color("black")
    pen.teleport(0, 0)
    pen.goto(1, 0)

    for node in graph.nodes:
        if current_level == node.level:
            index += 1
        else:
            index = 0
            current_level = node.level
            nodes_at_level = graph.count_nodes_in_level(current_level)

        coordinates[node.num] = (-600 + 1000 / (nodes_at_level + 1) * (index + 1),
                                 size * 40 - 80 * current_level)

    for k in coordinates.keys():
        for v in graph.nodes[k].get_neighbors():
            label = ""
            if (graph.nodes[v], graph.nodes[k]) not in visited_edges:
                if graph.nodes[k].receiver == v and int(graph.nodes[k].textOnSend) <= iteration:
                    label = graph.nodes[k].textOnSend
                visited_edges.append((graph.nodes[k], graph.nodes[v]))
                draw_edge(graph.nodes[k], graph.nodes[v], label)

        for v in graph.nodes[k].get_parents():
            label = ""
            if (graph.nodes[v], graph.nodes[k]) not in visited_edges:
                if graph.nodes[k].receiver == v and int(graph.nodes[k].textOnSend) <= iteration:
                    label = graph.nodes[k].textOnSend
                visited_edges.append((graph.nodes[k], graph.nodes[v]))
                draw_edge(graph.nodes[k], graph.nodes[v], label)

    color_map = {}
    for k in solution.keys():
        for source, target in solution[k]:
            if k <= iteration:
                color_map[source] = "green"
                color_map[target] = "blue" if k == iteration else "royalblue"
            else:
                color_map.setdefault(source, "black")
                color_map.setdefault(target, "black")

    for node_id, color in color_map.items():
        draw_node(graph.nodes[node_id], color)
    draw_max_slot_label(max(solution.keys()))
    canvas.update()

def save_graph():
    popup = TK.Toplevel(root)
    popup.title("Graph Name")
    popup.grab_set()

    TK.Label(popup, text="Enter a name for the graph:").pack(padx=10, pady=10)
    name_entry = TK.Entry(popup)
    name_entry.pack(padx=10, pady=5)

    def confirm():
        name = name_entry.get()
        if name:
            save(graph, name)
            popup.destroy()
        else:
            TK.messagebox.showwarning("Error", "Name cannot be empty.")

    TK.Button(popup, text="Save", command=confirm).pack(pady=10)

def load_graph(index):
    global graph, iteration
    graph = load(index)
    iteration = 0
    generate(True)

def load_list():
    popup = TK.Toplevel(root)
    popup.title("Select Graph")
    popup.grab_set()
    frame = TK.Frame(popup)
    frame.grid(padx=10, pady=10)
    names = loadNumber()
    for i, name in enumerate(names):
        TK.Button(frame, text=f"Graph {name}",
                  command=lambda i=i: load_graph_and_close(i, popup)).grid(row=i // 4, column=i % 4)

def load_graph_and_close(index, popup):
    load_graph(index)
    popup.destroy()

# Navigation
def scroll_up(event): canvas.yview_scroll(-10, "units")
def scroll_down(event): canvas.yview_scroll(10, "units")
def scroll_mouse(event): canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
def step_forward(event):
    global iteration
    if solution and iteration < max(solution.keys()):
        iteration += 1
        draw()
def step_backward(event):
    global iteration
    if solution and iteration >= 0:
        iteration -= 1
        draw()
def jump_end(event):
    global iteration
    iteration = max(solution.keys())
    draw()
def jump_start(event):
    global iteration
    iteration = -1
    draw()

# UI Layout
TK.Button(root, text="Save", command=save_graph).grid(column=0, row=0)
TK.Button(root, text="Generate", command=generate).grid(column=1, row=0)
TK.Button(root, text="Load", command=load_list).grid(column=2, row=0)
method_menu.grid(column=3, row=0)

TK.Label(root, text="Levels:").grid(column=4, row=0)
size_entry.grid(column=5, row=0)

TK.Label(root, text="Nodes/Level:").grid(column=6, row=0)
per_level_entry.grid(column=7, row=0)

canvas.grid(column=0, row=1, columnspan=8)

# Bindings clavier
canvas.bind_all("<Up>", scroll_up)
canvas.bind_all("<Down>", scroll_down)
canvas.bind_all("<MouseWheel>", scroll_mouse)
canvas.bind_all("<Left>", step_backward)
canvas.bind_all("<Right>", step_forward)
canvas.bind_all("<F>", jump_end)
canvas.bind_all("<D>", jump_start)
root.bind("<Return>", lambda e: generate())

root.mainloop()
