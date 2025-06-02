from random import randint


class Sommet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.voisin = []
        self.color = "black"
        self.state = None
        self.text = ""

    def get_coordoonees(self):
        return (self.x, self.y)

    def get_voisins(self):
        return self.voisin

    def add_voisin(self, sommet):
        if not sommet in self.voisin:
            self.voisin.append(sommet)
            sommet.voisin.append(self)
        # else:
        #     print("deja dans la liste")


def genererGraphe(niveau):
    startNiv = 0
    g = []
    s = Sommet(0, 200)
    s.color = "red"
    g.append(s)
    for n in range(niveau):
        endNiv = len(g)
        nbSommets = randint(1,4)
        prec = None
        for i in range(nbSommets):
            s=Sommet(-200 + 400/(nbSommets+1) * (i+1), 200 - 80*(n+1))
            g.append(s)
            if(prec is not None):
                if randint(0,2) == 2:
                    s.add_voisin(prec)
            prec = s

        dejaFait = []
        for sommet in range(endNiv, endNiv+nbSommets):
            sn = g[sommet]
            nbconnection = randint(1, endNiv - startNiv)
            # sn.text = nbconnection
            for i in range(nbconnection):
                sn1 = g[randint(startNiv, endNiv-1)]
                if(not (sn, sn1) in dejaFait):
                    dejaFait.append((sn, sn1))
                    sn.add_voisin(sn1)
        # for sommet in range(startNiv, endNiv):
        #     for
        startNiv = len(g)-nbSommets
    return g