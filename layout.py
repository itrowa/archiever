from DCEL import *

dcel = DCEL()
# Create the six vertices A--F: 
A = dcel.newVertex(Vector(0, 0, 0))
B = dcel.newVertex(Vector(100, 0, 0))
C = dcel.newVertex(Vector(100, 100, 0));
D = dcel.newVertex(Vector(0, 100, 0));

# Create a face for the inner face; Note: the outer face is dcel.outerFace
f = dcel.newFace()

# Create the six half-edges for inner face
AB = dcel.newHalfEdge(A, f);
BC = dcel.newHalfEdge(B, f);
CD = dcel.newHalfEdge(C, f);
DA = dcel.newHalfEdge(D, f);

# Make sure you set an incident half edge for f: 
f.incidentEdge = AB;

# Set up the next/prev pointers correctly for the face: 
AB.next = BC 
BC.prev = AB
BC.next = CD 
CD.prev = BC
CD.next = DA 
DA.prev = CD
DA.next = AB 
AB.prev = DA

# Create the half-edges for the outer face
AD = dcel.newHalfEdge(A, dcel.outerFace);
DC = dcel.newHalfEdge(D, dcel.outerFace);
CB = dcel.newHalfEdge(C, dcel.outerFace);
BA = dcel.newHalfEdge(B, dcel.outerFace);

# Make sure you set an incident half-edge for the outer face: 
dcel.outerFace.incidentEdge = AD;

# Set up the next/prev pointers correctly for the face: 
AD.next = DC
DC.prev = AD
DC.next = CB
CB.prev = DC
CB.next = BA
BA.prev = CB
BA.next = AD
AD.prev = BA


AB.twin = BA
BA.twin = AB
BC.twin = CB
CB.twin = BC
CD.twin = DC
DC.twin = CD
DA.twin = AD
AD.twin = DA


############################################################
############################################################
A.moveTo(Vector(-1800,0,0))
B.moveTo(Vector(5900,0,0))
C.moveTo(Vector(5900,8000,0))
D.moveTo(Vector(-1800,8000,0))

e = dcel.getHeById(3)
print(e)
E = dcel.splitInPlace(e)

# # create and move Vertex E
# E = dcel.splitInPlace(AB)
# E.moveTo(Vector(2100,0,0))

# # create and move Vertex F
# F = dcel.splitInPlace(DC)
# F.moveTo(Vector(2100,8000,0))

# # create new names
# E1 = AB
# E2 = E1.next.next.next

# #  split face
# dcel.splitFace(E1, E2)

# # slide edge
# dcel.slideEdge(E1.twin, 300)
dcel.draw()