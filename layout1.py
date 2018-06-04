from DCEL import *
# from generation import FaceReq

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

####################################################
# modify it into a house plan

E1 = AB

A.moveTo(Vector(-1800,0,0))
B.moveTo(Vector(5900,0,0))
C.moveTo(Vector(5900,8000,0))
D.moveTo(Vector(-1800,8000,0))

E = dcel.splitInPlace(AB)
E.moveTo(Vector(2100,0,0))
F = dcel.splitInPlace(DC)
E2 = E1.next.next.next
F.moveTo(Vector(2100,8000,0))

dcel.splitFace(E1, E2)
dcel.slideEdge(E2.twin, 1290)


G = dcel.splitInPlace(E2.next)
G.moveTo(Vector(-1800, 8000,0))
dcel.splitFace(E2.prev, E2.next.next)

E3 = E2.next.next.twin
H = dcel.splitInPlace(E1.next)
I = dcel.splitInPlace(E1.prev.twin)
H.moveTo(Vector(5900, 2640, 0))
I.moveTo(Vector(2100, 2640, 0))
dcel.splitFace(E1.next.next, E1.prev)

E4 = E1.next
J = dcel.splitInPlace(E1)
K = dcel.splitInPlace(E4)
J.moveTo(Vector(4500, 0, 0))
K.moveTo(Vector(5900, 900, 0))
dcel.splitFace(E1, E4)

L = dcel.splitInPlace(E1.prev)
L.moveTo(Vector(4500, 900, 0))

M = dcel.splitInPlace(E2)
N = dcel.splitInPlace(E2.next.next)
M.moveTo(Vector(-530, 9300, 0))
N.moveTo(Vector(-530, 8000, 0))
dcel.splitFace(E2, E2.next.next.next)

E5 = E2.next.next.twin
O = dcel.splitInPlace(E5.next)
P = dcel.splitInPlace(E5.prev.prev)
O.moveTo(Vector(-1800, 4200, 0))
P.moveTo(Vector(2100, 4200, 0))
dcel.splitFace(E5.next.next, E5.prev.prev)

Q = dcel.splitInPlace(E5.next.next)
Q.moveTo(Vector(0, 4200, 0))
dcel.slideEdge(E5.next.next, 1100)

E6 = E5.next.next.next.next
E7 = E6.twin.prev.prev.prev

R = dcel.splitInPlace(E7)
R.moveTo(Vector(0, 0, 0))
dcel.splitFace(E6.twin.next, E7)

E8 = E7.prev.twin.prev
dcel.slideEdge(E8, 1000)
S = dcel.splitInPlace(E8)
S.moveTo(Vector(500,0,0), relative=True)
dcel.slideEdge(E8.prev, 800)

T = dcel.splitInPlace(E7.prev.prev)
U = dcel.splitInPlace(E7.next)
T.moveTo(Vector(0, 1800, 0))
U.moveTo(Vector(2100, 1800, 0))
dcel.splitFace(E7.prev.prev, E7.next.next)

# ad-hoc point position adjustment
for v in dcel.vertices:
    if v.coord.y == 9290:
        v.coord.y = 9300

# setting function for each face.
F3 = dcel.getFaceById(3)
F3.fun = "BA"
F6 = dcel.getFaceById(6)
F6.fun = "EQ"
F10 = dcel.getFaceById(10)
F10.fun = "EH"
F8 = dcel.getFaceById(8)
F8.fun = "D"
F9 = dcel.getFaceById(9)
F9.fun = "K"
F2 = dcel.getFaceById(2)
F2.fun = "L"
F5 = dcel.getFaceById(5)
F5.fun = "BR"
F4 = dcel.getFaceById(4)
F4.fun = "BL"
F7 = dcel.getFaceById(7)
F7.fun = "EQ"

# function configuration setting:

# r1 = FaceReq("BR", 25000000)
# r2 = FaceReq("K",   8000000)
# r3 = FaceReq("L",  24000000)
# r4 = FaceReq("D",  15000000)
# r5 = FaceReq("BA",  3000000)
# r6 = FaceReq("EH",  3000000, direct_sunlight=False)
# r7 = FaceReq("BL",  4000000)


# dcel.draw()
