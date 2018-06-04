from vectors import Point, Vector

class Patch:
    def __init__(self):
        pass

    def add_patch(self):

class Vert:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = [];

class Poly:
    def __init__(self, verts):
        self.verts = verts

    # how to add just one vertice?
    def addEdge(self, u, v):
        self.verts.

# these are points
p1 = Vert(0, 9)
p2 = Vert(0, 3)
p3 = Vert(0, 0)
p4 = Vert(5, 0)
p5 = Vert(8, 0)
p6 = Vert(8, 3)
p7 = Vert(8, 9)
p8 = Vert(5, 9)
p9 = Vert(5, 3)

# these are polygons(rects)
a = Poly((p1, p2, p9, p8))
b = Poly((p2, p3, p5, p9))
c = Poly((p9, p4, p5, p6))
d = Poly((p8, p9, p6, p7))

geo = [a, b, c, d]

# finding p8-p9
def find_edge(polygon, x, y):
    """ find edge x-y in polygon. """
    for i in range(len(geo)):
        if i == 0:
            pass
        elif i == len(geo):
            pass
        else:
            if geo(i) == x:
                if geo(i-1) == y or geo(i+1) == y:

