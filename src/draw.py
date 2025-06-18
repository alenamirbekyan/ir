import math
import turtle as turtle
import tkinter as TK

from method.heuristic import Heuristic
from method.sda import SDA
from save import *
from summit import generate_graph, shortest_path_tree, generate_scatter_plot, lose_time_summit

# Default values
size = 5
per_level = 5
method = Heuristic()
max_solution = 0
root = TK.Tk()
root.title("Sensor Protocol Visualizer")
container = TK.Frame(root)



# Canvas & Turtle
canvas = turtle.ScrolledCanvas(container, width=1280, height=700)
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
shortest_path = None

# Dropdown for method
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

# Dropdown for generation mode
generation_mode = TK.StringVar(root)
generation_mode.set("Level-Based")
generation_menu = TK.OptionMenu(root, generation_mode, "Level-Based", "Node-Based")

def update_generation_mode(*args):
    if generation_mode.get() == "Level-Based":
        level_label.config(text="Levels:")
    else:
        level_label.config(text="Nodes:")

generation_mode.trace_add("write", lambda *args: update_generation_mode())

# User entries for size and per_level
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
    global graph, solution, iteration, size, per_level, coordinates, max_solution, shortest_path

    try:
        size = int(size_entry.get())
        per_level = int(per_level_entry.get())
        screen.screensize(1280, size * 80 + 300)

    except ValueError:
        print("Size values must be integers.")
        return

    if not from_load:
        if generation_mode.get() == "Level-Based":
            graph = generate_graph(size, per_level)
        else:
            res = generate_scatter_plot(size, 100)
            graph = res[1]
            coordinates = res[0]


    shortest_path = shortest_path_tree(graph, graph.nodes[0], [], [])
    if not shortest_path:
        print("Shortest path is empty. The graph may be malformed.")
        solution = {}
        return

    solution = graph.resolution(shortest_path, method)
    if solution is None:
        print("No transmission plan found.")
        solution = {}
    else:
        max_solution = max(solution.keys())

    iteration = -1

    if generation_mode.get() == "Level-Based":
        calculate_coordinates()
    else:
        screen.screensize(10000,10000)
        draw()


def draw_max_slot_label(slot):
    pen.color("black")
    pen.teleport(-600, size * 40)
    pen.write(f"Total slots: {slot + 1}", align="left", font=("Arial", 12, "bold"))

def calculate_coordinates():
    global iteration, coordinates, screen

    coordinates = {}
    nodes_at_level = 0

    index_by_level = {}

    max_x = 0
    min_x = 0
    max_y = 0
    min_y = 0

    for node in graph.nodes:
        if node.level in index_by_level.keys():
            index_by_level[node.level] += 1
        else:
            index_by_level[node.level] = 0
        nodes_at_level = graph.count_nodes_in_level(node.level)

        x = -600 + 1000 / (nodes_at_level + 1) * (index_by_level[node.level] + 1)
        y = size * 40 - 80 * node.level

        if x>max_x:
            max_x = x
        elif x<min_x:
            min_x = x

        if y>max_y:
            max_y = y
        elif y<min_y:
            min_y = y

        coordinates[node.num] = (x,y)
    draw()

def draw():
    canvas.delete("all")
    pen.clear()

    pen.color("black")
    pen.teleport(0, 0)
    pen.goto(1, 0)

    global coordinates, graph
    visited_edges = []

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

# Keyboard navigation
def scroll_up(event): canvas.yview_scroll(-10, "units")
def scroll_down(event): canvas.yview_scroll(10, "units")
def scroll_mouse(event): canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
def step_forward(event):
    global iteration
    if solution and iteration < max_solution:
        iteration += 1
        draw()
def step_backward(event):
    global iteration
    if solution and iteration >= 0:
        iteration -= 1
        draw()

def jump_end(event):
    global iteration
    iteration = max_solution
    draw()

def jump_start(event):
    global iteration
    iteration = -1
    draw()

def recuit():
    global solution, graph, max_solution, iteration
    info = lose_time_summit(solution, graph)
    solution = graph.resolution(shortest_path, method, info[1])
    if solution is None:
        print("No transmission plan found.")
        solution = {}
    else:
        max_solution = max(solution.keys())
        iteration = max_solution
        draw()

easter_egg_state = 0
def easter_egg(event):
    global easter_egg_state
    easter_egg_code = "bakadam"

    if(easter_egg_code[easter_egg_state] == event.char):
        easter_egg_state+=1
    else:
        easter_egg_state = 0

    if(easter_egg_state == len(easter_egg_code)):
        image = TK.PhotoImage(file="../img/adam.png")
        easter_egg_state = 0

        canvas.create_image(0, 0, image=image)
        canvas.image = image

# UI Layout
TK.Button(root, text="Save", command=save_graph).grid(column=0, row=0)
TK.Button(root, text="Generate", command=generate).grid(column=1, row=0)
TK.Button(root, text="Load", command=load_list).grid(column=2, row=0)
method_menu.grid(column=3, row=0)

level_label = TK.Label(root, text="Levels:")
level_label.grid(column=4, row=0)
size_entry.grid(column=5, row=0)

TK.Label(root, text="Nodes/Level:").grid(column=6, row=0)
per_level_entry.grid(column=7, row=0)

generation_menu.grid(column=8, row=0)

canvas.grid(column=0, row=0)
container.grid(column=0, row=1, columnspan=9)

TK.Button(container, text="recuit simulé", command=recuit).grid(column=1, row=0)

# Bindings
canvas.bind_all("<Up>", scroll_up)
canvas.bind_all("<Down>", scroll_down)
canvas.bind_all("<MouseWheel>", scroll_mouse)
canvas.bind_all("<Left>", step_backward)
canvas.bind_all("<Right>", step_forward)
canvas.bind_all("<F>", jump_end)
canvas.bind_all("<D>", jump_start)
canvas.bind_all("<Key>", easter_egg)
root.bind("<Return>", lambda e: generate())

root.mainloop()
