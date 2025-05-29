from model.model import Model

mymodel=Model()
mymodel.buildGraph(120)
nodi, archi= mymodel.getGraphDetails()
print(nodi)
print(archi)