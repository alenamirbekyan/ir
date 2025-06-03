import math
import time
import turtle as turtle
from random import randint

from sommet import genererGraphe, Sommet, courtChemain

t = turtle.Turtle()
t.ht()
t.color('black')
t.fillcolor('blue')
t.speed(0)

win = turtle.Screen()
win.setup(600, 600)
win.tracer(0, 0)


def lighten_color(color_name, factor=0.5):
    # Récupérer le code RGB 0-65535 depuis le nom de couleur
    rgb_16bit = win._root.winfo_rgb(color_name)
    # Convertir en 0-255
    rgb_8bit = [int(c / 65535 * 255) for c in rgb_16bit]

    # Appliquer un éclaircissement vers le blanc
    light_rgb = [int(c + (255 - c) * factor) for c in rgb_8bit]

    # Convertir en hexadécimal
    return '#%02x%02x%02x' % tuple(light_rgb)

def draw_sensor(sensor):
    t.teleport(coordonnees[sensor][0] - 10, coordonnees[sensor][1] - 16.8)
    t.color(sensor.color)
    print(sensor.color)
    t.setheading(0)
    t.fillcolor(sensor.color)
    t.fillcolor(lighten_color(sensor.color))
    t.begin_fill()
    for i in range(6):
        t.forward(20)
        t.left(60)
    t.end_fill()


def draw_line(sensor1, sensor2, text, couleur="black"):
    t.teleport(coordonnees[sensor1][0], coordonnees[sensor1][1])
    t.color(couleur)
    t.goto(coordonnees[sensor2][0], coordonnees[sensor2][1])
    distanceX = (coordonnees[sensor2][0] + coordonnees[sensor1][0]) / 2
    distanceY = (coordonnees[sensor2][1] + coordonnees[sensor1][1]) / 2
    t.teleport(distanceX, distanceY)
    t.write(text, align="center")

def clear():
    t.teleport(-800, -800)
    t.color("white")
    t.setheading(0)
    t.fillcolor("white")
    t.begin_fill()
    for i in range(4):
        t.forward(1600)
        t.left(90)
    t.end_fill()


colors = ["red", "blue", "black", "green"]

# print(courtChemain(sommets[0]))

def generer():
    voisins = []
    global t
    t.clear()
    global g
    g = genererGraphe(6, 7)
    global coordonnees
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
        coordonnees[s] = -600 + 1200/(nbElemNiveau+1) * (i+1), 200 - 80*(niv)

    for k in coordonnees.keys():
        for v in k.get_voisins():
            if not (v,k) in voisins:
                voisins.append((k,v))
                draw_line(k, v, "")
        for v in k.get_parent():
            if not (v,k) in voisins:
                voisins.append((k,v))
                draw_line(k, v, "")

    for k in coordonnees.keys():
        draw_sensor(k)
    win.update()

generer()
    
coordonnees = {}

turtle.listen()

# turtle.onkeypress(generer, "space")
turtle.onkeypress(generer, "Return")

turtle.mainloop()