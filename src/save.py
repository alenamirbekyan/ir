import json

from sommet import Graph, Sommet


def save(g, name):
    if g is not None:
        with open('saveFile.json', mode='r+') as file:
            data = json.load(file)
            res = g.toString()
            new_graph = json.loads(res)
            new_graph["name"] = name
            data["nombre"]+=1
            data["graphes"].append(new_graph)
            file.seek(0)
            file.write(json.dumps(data, indent=4))
            file.truncate()

def loadNumber():
    with open('saveFile.json', mode='r') as file:
        data = json.load(file)
        res = []
        for i in range(data["nombre"]):
            res.append(data["graphes"][i]["name"])
        return res

def load(num):
    with open('saveFile.json', mode='r') as file:
        data = json.load(file)
        res = []
        hauteur = data["graphes"][num]["hauteur"]
        for s in data["graphes"][num]["sommet"]:
            sommet = Sommet(int(s["niv"]), int(s["num"]))
            sommet.color = s["color"]
            sommet.enfants = s["enfants"]
            sommet.voisin = s["voisins"]
            sommet.parent = s["parents"]
            res.append(sommet)
        return Graph(res, hauteur)
