from math import trunc
from random import randint


class Graph:
    def __init__(self, sommets, hauteur):
        self.sommets = sommets
        self.min = {}
        self.hauteur = hauteur
        self.bornInf()

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

    def resolution(self, court):
        nbEnf = {}
        for s in self.sommets:
            nbEnf[s.num] = len(s.get_enfant())*5 + len(s.get_voisins()) + len(s.get_parent())
        sorted_by_values = dict(sorted(nbEnf.items(), key=lambda item: item[1]))
        envoyer = []
        occuper = []
        i=0
        while i<len(self.sommets)-1:
            occuper = []
            for k in sorted_by_values.keys():
                if(k not in occuper and k not in envoyer):
                    enfants = self.sommets[k].get_enfant()
                    par = self.sommets[k].get_parent()
                    ok = True
                    for enf in enfants:
                        if enf not in envoyer:
                            if (k, enf) in court:
                                ok = False
                    if ok:
                        for p in par:
                            if(p not in envoyer and p not in occuper):
                                #codition: si parant d'enfant, l'enfant doit avoir un autre parant
                                if ok:
                                    self.sommets[p].color = "blue"
                                    self.sommets[k].color = "green"
                                    self.sommets[k].textSiEnvoi = i
                                    self.sommets[k].destinataire = p
                                    envoyer.append(k)
                                    occuper.append(p)
                                    break
                            else:
                                voisins = self.sommets[k].get_voisins()
                                for v in voisins:
                                    if v not in occuper and v not in envoyer:
                                        self.sommets[v].color = "blue"
                                        self.sommets[k].color = "green"
                                        self.sommets[k].textSiEnvoi = i
                                        self.sommets[k].destinataire = v
                                        envoyer.append(k)
                                        occuper.append(v)
                                        break
            i+=1

    def bornInf(self):
        numSommet = 0
        for i in range(self.hauteur):
            while self.sommets[numSommet].niveau <= i:
                numSommet+=1

    def toString(self):
        res=("{ \"hauteur\":"+str(self.hauteur)+","
             "\"sommet\":[")
        first = True
        for s in self.sommets:
            if not first:
                res+=","
            first = False
            res+="{"+s.toString()+"}"
        return res+"]}\n"


class Sommet:
    def __init__(self, niv, num):
        self.num = num
        self.niveau = niv
        self.voisin = []
        self.parent = []
        self.enfants = []
        self.color = "black"
        self.state = None
        self.text = ""
        self.textSiEnvoi = ""
        self.destinataire = None

    def get_voisins(self):
        return self.voisin

    def add_voisin(self, sommet):
        if not sommet.num in self.voisin:
            self.voisin.append(sommet.num)
            sommet.voisin.append(self.num)

    def add_parent(self, par):
        self.parent.append(par.num)
        par.add_enfant(self)

    def add_enfant(self, enf):
        self.enfants.append(enf.num)

    def get_parent(self):
        return self.parent

    def get_enfant(self):
        return self.enfants

    def toString(self):
        res="\"num\":"+str(self.num)+","
        res+="\"niv\":"+str(self.niveau)+","
        res+="\"color\":\""+self.color+"\","
        res+="\"parents\":["
        first = True
        for p in self.parent:
            if not first:
                res+=","
            first = False
            res+=str(p)
        res+="],"
        res += "\"voisins\":["
        first = True
        for p in self.voisin:
            if not first:
                res+=","
            first = False
            res +=str(p)
        res += "],"
        res+="\"enfants\":["
        first = True
        for p in self.enfants:
            if not first:
                res+=","
            first = False
            res+=str(p)
        res+="]"
        return res


def genererGraphe(niveau, nbPoint):
    num = 0
    startNiv = 0
    g = []
    s = Sommet(0, num)
    s.color = "red"
    g.append(s)
    for n in range(1, niveau+1):
        endNiv = len(g)
        nbSommets = randint(1,nbPoint)
        prec = None
        for i in range(nbSommets):
            num+=1
            s=Sommet(n, num)
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
    return Graph(g, niveau)

def courtChemain(g, sommet, connection, enfant_utilise):
    for voisin in sommet.get_enfant():
        if not voisin in enfant_utilise:
            connection.append((sommet.num, voisin))
            enfant_utilise.append(voisin)
            connection = courtChemain(g, g.sommets[voisin], connection, enfant_utilise)
    return connection

