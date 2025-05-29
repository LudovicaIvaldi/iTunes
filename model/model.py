import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allNodi = []
        self._grafo=nx.Graph()
        self._idMapAlbum = {}
        self._bestSet={}
        self._maxLen=0


    def buildGraph(self, durataMin):
        self._grafo.clear()
        self._allNodi=DAO.getAlbums(durataMin)
        self._grafo.add_nodes_from(self._allNodi)
        self._idMapAlbum = {n.AlbumId:n for n in self._allNodi}
        self._allEdges=DAO.getAllEdges(self._idMapAlbum)
        self._grafo.add_edges_from(self._allEdges)


    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getAllNodes(self):
        return list(self._grafo.nodes())

    def getInfoConnessa(self,a1):
        cc= nx.node_connected_component(self._grafo,a1)
        return len(cc), self.getDurataTot(cc)

    def getDurataTot(self, listOfNodes):
        sumDurata = 0
        for n in listOfNodes:
            sumDurata+=n.dTot
        return sumDurata
        #return sum([n.dTot for n in listOfNodes])


    def getSetOfNodes(self,a1, soglia):
        self._bestSet = {}
        self._maxLen = 0
        parziale={a1}
        cc=nx.node_connected_component(self._grafo,a1)
        cc.remove(a1)
        for n in cc:
            parziale.add(n)
            cc.remove(n)
            self._ricorsione(parziale,cc,soglia)
            cc.add(n)
            parziale.remove(n)
        return self._bestSet, self.getDurataTot(self._bestSet)

    def _ricorsione(self,parziale,rimanenti,soglia):
        #parziale deve essere ammissibile -> se viola i vincoli devo scartare tutta la linea di soluzioni
        #che passa di lì
        if self.getDurataTot(parziale)>soglia:
            return
            #blocco questa linea di esplorazione
        if len(parziale)>self._maxLen:
            self._maxLen = len(parziale)
            self._bestSet=copy.deepcopy(parziale)

        #se è ammissibile parziale allora guardo se è ottima -> non è di terminazione
        #aggiungo e faccio ricorsione
        for n in rimanenti:
            parziale.add(n)
            rimanenti.remove(n)
            self._ricorsione(parziale,rimanenti,soglia)
            parziale.remove(n)
            rimanenti.add(n)

