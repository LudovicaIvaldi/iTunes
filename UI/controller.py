import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceDD=None

    def handleCreaGrafo(self, e):
        dMinTxt=self._view._txtInDurata.value
        if dMinTxt=="":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione inserire valore minimo di durata"))
            self._view.update_page()
            return
        try:
            dMin=int(dMinTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione inserire valore intero"))
            self._view.update_page()
            return
        self._model.buildGraph(dMin)
        nodi, archi = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.txt_result.controls.append(ft.Text(f"numero di nodi {nodi} e numero di archi {archi}"))
        self._fillDD(self._model.getAllNodes())
        self._view.update_page()



    def _fillDD(self, listaOfNodes):
        listaOfNodes.sort(key=lambda n: n.Title)
        for x in listaOfNodes:
            self._view._ddAlbum.options.append(ft.dropdown.Option(text=x.Title,
                                                       data=x,
                                                       on_click=self._readDDValue), listaOfNodes)


    def _readDDValue(self, e):
        if e.control.data is None:
            print("error in reading dd")
            self._choiceDD=None
        self._choiceDD=e.control.data

    # def getSelectedAlbum(self, e):
    #     pass

    def handleAnalisiComp(self, e):
        if self._choiceDD is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione selezionare un album"))
            self._view.update_page()
            return

        size, dTotCC=self._model.getInfoConnessa(self._choiceDD)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa che contiene {self._choiceDD} ha {size} nodi e una dorata totale di {dTotCC} minuti"))
        self._view.update_page()


    def handleGetSetAlbum(self, e):
        sogliaTxt=self._view._txtInSoglia.value
        if sogliaTxt=="":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione selezionare una soglia massima"))
            self._view.update_page()
            return
        try:
            soglia=int(sogliaTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Devi mettere un numero intero"))
            self._view.update_page()
            return
        if self._choiceDD is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione selezionare un album"))
            self._view.update_page()
            return

        setOfNodes, sumDurata=self._model.getSetOfNodes(self._choiceDD,soglia)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Set di album trovato di dimensione {len(setOfNodes)} e di durata totalre {sumDurata} minuti"))
        for a in setOfNodes:
            self._view.txt_result.controls.append(
                ft.Text(a))

        self._view.update_page()
