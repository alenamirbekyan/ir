import time
import turtle as turtle
from random import randint

from sommet import genererGraphe, Sommet

t = turtle.Turtle()
t.ht()
t.color('black')
t.fillcolor('blue')
t.speed(0)

win = turtle.Screen()
win.setup(600, 600)
win.tracer(0)


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
    t.teleport(sensor.x - 10, sensor.y - 16.8)
    t.color(sensor.color)
    t.setheading(0)
    t.fillcolor(lighten_color(sensor.color))
    t.begin_fill()
    for i in range(6):
        t.forward(20)
        t.left(60)
    t.end_fill()


def draw_line(sensor1, sensor2, text, couleur="black"):
    t.teleport(sensor1.x, sensor1.y)
    t.color(couleur)
    t.goto(sensor2.x, sensor2.y)
    distanceX = (sensor2.x + sensor1.x) / 2
    distanceY = (sensor2.y + sensor1.y) / 2
    t.teleport(distanceX, distanceY)
    t.write(text, align="center")

def clear():
    t.teleport(-400, -400)
    t.color("white")
    t.setheading(0)
    t.fillcolor("white")
    t.begin_fill()
    for i in range(4):
        t.forward(800)
        t.left(90)
    t.end_fill()

# sommets = []
#
# s1 = Sommet(0, 0)
#
# s2 = Sommet(60, 0)
#
# s1.add_voisin(s2)
#
# sommets.append(s1)
# sommets.append(s2)


colors = ["red", "blue", "black", "green"]

sommets = genererGraphe(4)

def generer():
    global sommets
    sommets = genererGraphe(4)

while True:

    clear()
    turtle.listen()

    # turtle.onkeypress(generer, "space")
    turtle.onkeypress(generer, "Return")

    voisins = []

    for s in sommets:
        for v in s.get_voisins():
            if not (v,s) in voisins:
                voisins.append((s,v))
                draw_line(s, v, "")
        draw_sensor(s)


    win.update()
