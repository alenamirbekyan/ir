from method.method import Methode

class Heuristique(Methode):

    def resoudre(self, graphe, court=[]):
        nbEnf = {}
        for s in graphe.sommets:
            nbEnf[s.num] = len(s.get_enfant()) * 5 + len(s.get_voisins()) + len(s.get_parent())
        sorted_by_values = dict(sorted(nbEnf.items(), key=lambda item: item[1]))
        envoyer = []
        i = 0
        while i < len(graphe.sommets) - 1:
            occuper = []
            for k in sorted_by_values.keys():
                if (k not in occuper and k not in envoyer):
                    enfants = graphe.sommets[k].get_enfant()
                    par = graphe.sommets[k].get_parent()
                    ok = True
                    for enf in enfants:
                        if enf not in envoyer:
                            if (k, enf) in court:
                                ok = False
                    if ok:
                        for p in par:
                            if (p not in envoyer and p not in occuper):
                                # codition: si parant d'enfant, l'enfant doit avoir un autre parant
                                graphe.sommets[p].color = "blue"
                                graphe.sommets[k].color = "green"
                                graphe.sommets[k].textSiEnvoi = i
                                graphe.sommets[k].destinataire = p
                                envoyer.append(k)
                                occuper.append(p)
                                break
                            else:
                                voisins = graphe.sommets[k].get_voisins()
                                for v in voisins:
                                    if v not in occuper and v not in envoyer:
                                        graphe.sommets[v].color = "blue"
                                        graphe.sommets[k].color = "green"
                                        graphe.sommets[k].textSiEnvoi = i
                                        graphe.sommets[k].destinataire = v
                                        envoyer.append(k)
                                        occuper.append(v)
                                        break
            i += 1