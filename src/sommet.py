from random import randint

class Graph:
    def __init__(self, sommets):
        self.sommets = sommets

    def chargerGraph(self, fichier, ligne):
        pass

    def sauvgarderGraph(self, fichier):
        pass

    def nbElemNiv(self, niv):
        res = 0
        for s in self.sommets:
            if s.niveau == niv:
                res+=1
            elif s.niveau>niv:
                return res
        return res


class Sommet:
    def __init__(self, niv):
        self.niveau = niv
        self.voisin = []
        self.parent = []
        self.enfants = []
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

    def add_parent(self, par):
        self.parent.append(par)
        par.add_enfant(self)

    def add_enfant(self, enf):
        self.enfants.append(enf)

    def get_parent(self):
        return self.parent

    def get_enfat(self):
        return self.enfants

def genererGraphe(niveau, nbPoint):
    startNiv = 0
    g = []
    s = Sommet(0)
    s.color = "red"
    g.append(s)
    for n in range(1, niveau+1):
        endNiv = len(g)
        nbSommets = randint(1,nbPoint)
        prec = None
        for i in range(nbSommets):
            s=Sommet(n)
            g.append(s)
            if(prec is not None):
                if randint(0,2) == 2:
                    s.add_voisin(prec)
            prec = s

        dejaFait = []
        for sommet in range(endNiv, endNiv+nbSommets):
            sn = g[sommet]
            nbconnection = randint(1, endNiv - startNiv)
            if(nbconnection > 3):
                nbconnection = 3
            # sn.text = nbconnection
            for i in range(nbconnection):
                sn1 = g[randint(startNiv, endNiv-1)]
                if(not (sn, sn1) in dejaFait):
                    dejaFait.append((sn, sn1))
                    sn.add_parent(sn1)
        # for sommet in range(startNiv, endNiv):
        #     for
        startNiv = len(g)-nbSommets
    return Graph(g)

def courtChemain(sommet, connection = []):
    for voisin in sommet.get_voisins():
        if(not (voisin, sommet) in connection and not (sommet, voisin) in connection):
            connection.append((sommet, voisin))
            return courtChemain(voisin, connection)