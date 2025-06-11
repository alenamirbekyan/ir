import math
import turtle as turtle
import tkinter as TK

from method.heuristic import Heuristique
from method.sda import SDA

from save import *

from summit import generate_graph, courtChemain

size = 50
method = Heuristique()
# method = SDA()

root = TK.Tk()
# root.attributes('-fullscreen', True)
cv = turtle.ScrolledCanvas(root, width=1920, height=800)

screen = turtle.TurtleScreen(cv)
screen.screensize(1920,size * 80 + 400) #added by me
t = turtle.RawTurtle(screen)
t.hideturtle()
t.speed(0)
screen.tracer(0,0)
t.hideturtle()

g = None
coordonnees = {}
solution = {}
iteration = 0


def lighten_color(color_name, factor=0.5):
    rgb_16bit = root.winfo_rgb(color_name)
    rgb_8bit = [int(c / 65535 * 255) for c in rgb_16bit]
    light_rgb = [int(c + (255 - c) * factor) for c in rgb_8bit]
    return '#%02x%02x%02x' % tuple(light_rgb)

def draw_sensor(sensor, color):
    t.teleport(coordonnees[sensor.num][0] - 10, coordonnees[sensor.num][1] - 16.8)
    t.color(color)
    t.setheading(0)
    t.fillcolor(color)
    t.fillcolor(lighten_color(color))
    t.begin_fill()
    for i in range(6):
        t.forward(20)
        t.left(60)
    t.end_fill()
    t.fillcolor(color)
    t.teleport(coordonnees[sensor.num][0], coordonnees[sensor.num][1])
    t.write(sensor.num, align="center")

def draw_line(sensor1, sensor2, text, couleur="black"):
    x1, y1 = coordonnees[sensor1.num]
    x2, y2 = coordonnees[sensor2.num]

    t.teleport(x1, y1)
    t.color(couleur)
    t.goto(x2, y2)

    if text != "":
        dx = x2 - x1
        dy = y2 - y1
        angle = math.degrees(math.atan2(dy, dx))

        # Position du texte légèrement décalée dans la direction du trait
        distance = 25
        t.teleport(x1 + math.cos(math.radians(angle)) * distance,
                   y1 + math.sin(math.radians(angle)) * distance)

        t.write(text, align="center")

def generate(charge = False):
    global g
    global solution
    global iteration

    if(not charge):
        g = generate_graph(size, 7)
    court_chemain = courtChemain(g, g.sommets[0], [], [])
    solution = g.resolution(court_chemain, method)
    iteration = -1
    print(solution)

    draw()

def test():
    t.color("black")
    t.teleport(0, 0)
    t.goto(1, 0)

def draw():
    global iteration
    global coordonnees
    global g
    global solution

    cv.delete("all")
    voisins = []
    coordonnees = {}
    niv = math.inf
    nbElemNiveau = 0
    i = 0
    for s in g.sommets:
        if niv == s.niveau:
            i+=1
        else:
            i=0
            niv = s.niveau
            nbElemNiveau = g.nbElemNiv(niv)
        coordonnees[s.num] = -1000 + 1600/(nbElemNiveau+1) * (i+1), size*40 - 80*(niv)

    test()
    for k in coordonnees.keys():
        for v in g.sommets[k].get_voisins():
            txt = ""
            if not (g.sommets[v],g.sommets[k]) in voisins:
                if g.sommets[k].destinataire == v and int(g.sommets[k].textSiEnvoi) <= iteration:
                    txt = g.sommets[k].textSiEnvoi
                voisins.append((g.sommets[k],g.sommets[v]))
                draw_line(g.sommets[k], g.sommets[v], txt)
        for v in g.sommets[k].get_parent():
            txt = ""
            if not (g.sommets[v],g.sommets[k]) in voisins:
                if g.sommets[k].destinataire == v and int(g.sommets[k].textSiEnvoi) <= iteration:
                    txt = g.sommets[k].textSiEnvoi
                voisins.append((g.sommets[k],g.sommets[v]))
                draw_line(g.sommets[k], g.sommets[v], txt)


    # for chemain in court_chemain:
    #     draw_line(g.sommets[chemain[0]], g.sommets[chemain[1]],"" , "red")

    colorSummit = {}

    for k in solution.keys():
        for summits in solution[k]:
            if(k<=iteration):
                colorSummit[summits[0]] = "green"
                if (k==iteration):
                    colorSummit[summits[1]] = "blue"
            else:
                if(summits[1] not in colorSummit.keys()):
                    colorSummit[summits[1]] = "black"
                if(summits[0] not in colorSummit.keys()):
                    colorSummit[summits[0]] = "black"


    for k in colorSummit.keys():
        draw_sensor(g.sommets[k], colorSummit[k])

    cv.update()

def saveGraph():
    popup = TK.Toplevel(root)
    popup.title("Nom du graphe")
    popup.grab_set()

    TK.Label(popup, text="Entrez un nom pour le graphe :").pack(padx=10, pady=10)
    name_entry = TK.Entry(popup)
    name_entry.pack(padx=10, pady=5)

    def confirm():
        global g
        nom = name_entry.get()
        if nom:
            save(g, nom)  # Appelle ta fonction de sauvegarde
            popup.destroy()
        else:
            TK.messagebox.showwarning("Erreur", "Le nom ne peut pas être vide.")

    TK.Button(popup, text="Enregistrer", command=confirm).pack(pady=10)

def load_graph(i):
    global g
    global iteration
    g=load(i)
    iteration = 0
    generate(True)

def load_liste():
    popup = TK.Toplevel(root)
    popup.title("Sélection du graphe")
    popup.grab_set()
    frame = TK.Frame(popup)
    frame.grid(padx=10, pady=10)
    nb = loadNumber()
    for i in range(len(nb)):
        name = nb[i]
        TK.Button(frame, text=f"Graphe {name}", command=lambda i=i: load(i)).grid(row=i // 4, column=i % 4)

    def load(i):
        load_graph(i)
        popup.destroy()

btn = TK.Button(root, text="Générer", command=generate)
btn.grid(column=1, row=0)

btnSave = TK.Button(root, text="Sauvegarder", command=saveGraph)
btnSave.grid(column=0, row=0)

btnLoad = TK.Button(root, text="Charger", command=load_liste)
btnLoad.grid(column=2, row=0)

cv.grid(column=0, row=1, columnspan=4)

def on_mousewheel_up(event):
    cv.yview_scroll(-10, "units")

def on_mousewheel_down(event):
    cv.yview_scroll(10, "units")

def on_mousewheel(event):
    cv.yview_scroll(int(-1 * (event.delta / 120)), "units")

def forward(event):
    global solution
    global iteration
    if solution != {} and iteration<max(solution.keys()):
        iteration+=1
        draw()

def backward(event):
    global solution
    global iteration
    if solution != {} and iteration>=0:
        iteration -= 1
        draw()

def end(event):
    global solution
    global iteration
    iteration =max(solution.keys())
    draw()

def start(event):
    global iteration
    iteration = -1
    draw()


cv.bind_all("<Up>", on_mousewheel_up)
cv.bind_all("<Down>", on_mousewheel_down)
cv.bind_all("<MouseWheel>", on_mousewheel)

cv.bind_all("<Left>", backward)
cv.bind_all("<Right>", forward)
cv.bind_all("<F>", end)
cv.bind_all("<D>", start)


root.bind("<Return>", lambda event: generate())

root.mainloop()