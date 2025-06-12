import json

from summit import Graph, Node


def save(g, name):
    if g is not None:
        with open('save_file.json', mode='r+') as file:
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
    with open('/Users/rudoniantonin/Documents/CESI/S8/IR/ir/src/save_file.json', mode='r') as file:
        data = json.load(file)
        res = []
        for i in range(data["nombre"]):
            res.append(data["graphes"][i]["name"])
        return res

def load(num):
    with open('/Users/rudoniantonin/Documents/CESI/S8/IR/ir/src/save_file.json', mode='r') as file:
        data = json.load(file)
        res = []
        height = data["graphes"][num]["height"]
        for s in data["graphes"][num]["node"]:
            node = Node(int(s["level"]), int(s["num"]))
            node.color = s["color"]
            node.childrens = s["childrens"]
            node.neighbors = s["neighbors"]
            node.parents = s["parents"]
            res.append(node)
        return Graph(res, height)
