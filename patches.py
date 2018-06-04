from vectors import Point, Vector
import networkx as nx
import numpy as nu
import matplotlib.pyplot as plt

class Patch:
    def __init__(self, w, d, coor, funType):
        self.w = w
        self.d = d
        self.coor = coor
        self.funType = funType
        
        # optional characteristics
        self.winArea = 0
        self.height = 2000
        self.enclosure = None

    def setWinArea(self, area):
        # in in square milimeters!
        self.winArea = area

    def setHeight(self, height):
        self.height = height

    def setEnclosure(self, enc):
        self.enclosure = enc

class PlanGraph:
    # a Plan dataset.
    def __init__(self):
        self.g = nx.Graph()

    def __repr__(self):
        return 'PlanGraph: <' + str(self.g.edges()) + '> with <' + str(self.g.nodes()) + '>'

    def addPatch(self, funArea):
        self.g.add_node(funArea)

    def addConn(self, edges):
        # edge: an tuple
        self.g.add_edge(*edges)

def get_init_data():
    # create g1 as example 
    p1 = Patch(1100, 1400, Point(2200, 2900, 0), 'E')
    p2 = Patch(2100, 1400, Point(3800, 3200, 0), 'BA')
    p3 = Patch(1100, 1600, Point(2200, 4400, 0), 'D')
    p4 = Patch(1100, 1600, Point(1100, 1400, 0), 'K')
    p5 = Patch(2100, 3100, Point(3800, 5400, 0), 'BR')
    p6 = Patch(2100, 1600, Point(1500, 6000, 0), 'L')

    g1 = PlanGraph()
    g1.addPatch(p1)
    g1.addPatch(p2)
    g1.addPatch(p3)
    g1.addPatch(p4)
    g1.addPatch(p5)
    g1.addPatch(p6)
    g1.addConn((p1,p2))
    g1.addConn((p1,p3))
    g1.addConn((p1,p4))
    g1.addConn((p3,p4))
    g1.addConn((p3,p5))
    g1.addConn((p3,p6))
    g1.addConn((p4,p6))

    return g1

if __name__ == '__main__':
    g1 = get_init_data()
    g2 = nx.dodecahedral_graph()
    nx.draw(g1.g)

    pylab.show()

