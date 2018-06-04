from DCEL import *

#####################################
# 测试slideEdge, mergeEdge函数.

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
A.moveTo(Vector(-1300,0,0))
B.moveTo(Vector(5300,0,0))
C.moveTo(Vector(5300,7000,0))
D.moveTo(Vector(-1300,7000,0))

E3 = dcel.getHeById(3)

#creat vertex 5 and move vertex 5
V5 = dcel.splitInPlace(E3)
V5.moveTo(Vector(3000,7000,0))
#creat vertex 6 and move vertex 6
V6 = dcel.splitInPlace(E3)
V6.moveTo(Vector(1000,7000,0))

# slideEdge E11
E11 = dcel.getHeById(11)
dcel.slideEdge(E11.twin, 1000)
dcel.slideEdge(E11.twin, 900)
dcel.slideEdge(E11.twin, 1100)

# splitFace E3 E9
E9 = dcel.getHeById(9)
dcel.splitFace(E3, E9)

#creat vertex 9 and move vertex 9
E1 = dcel.getHeById(1)
V9 = dcel.splitInPlace(E1) 
V9.moveTo(Vector(2000,0,0))

# slideEdge E8
E8 = dcel.getHeById(8)
dcel.slideEdge(E8, 1500)

# creat vertex 11 and move vertex 11
E18 = dcel.getHeById(18)
V11 = dcel.splitInPlace(E18)
V11.moveTo(Vector(2000,7000,0))

#creat vertex 12 and move vertex 12
E16 = dcel.getHeById(16)
V12 = dcel.splitInPlace(E16)
V12.moveTo(Vector(1000,8500,0))

#creat vertex 13 and move vertex 13
E13 = dcel.getHeById(13)
V13 = dcel.splitInPlace(E13)
V13.moveTo(Vector(3000,8500,0))

# splitFace E16 E13
dcel.splitFace(E13, E16)

#creat vertex 14 and move vertex 14
E29 = dcel.getHeById(29)
V14 = dcel.splitInPlace(E29)
V14.moveTo(Vector(2000,8500,0))

# splitFace E24 E29
E24 = dcel.getHeById(24)
dcel.splitFace(E24, E29)

# splitFace E18 E21
E21 = dcel.getHeById(21)
E18 = dcel.getHeById(18)
dcel.splitFace(E18, E21)

#creat vertex 15 and move vertex 15
E36 = dcel.getHeById(36)
V15 = dcel.splitInPlace(E36)
V15.moveTo(Vector(2000,3000,0))

#creat vertex 16 and move vertex 16
E4 = dcel.getHeById(4)
V16 = dcel.splitInPlace(E4)
V16.moveTo(Vector(-1300,3000,0))

# splitFace E4 E36
dcel.splitFace(E4, E36)

#creat vertex 17 and move vertex 7
V17 = dcel.splitInPlace(E36)
V17.moveTo(Vector(2000,4000,0))

#creat vertex 18 and move vertex 18
E39 = dcel.getHeById(39)
V18 = dcel.splitInPlace(E39)
V18.moveTo(Vector(-1300,4000,0))

# splitFace E39 E36
dcel.splitFace(E39, E36)

# slideEdge E36
dcel.slideEdge(E36.twin, 500)

#creat vertex 21 and move vertex 21
E2 = dcel.getHeById(2)
V21 = dcel.splitInPlace(E2)
V21.moveTo(Vector(5300,0,0))

# splitFace E2 E21
dcel.splitFace(E2, E21)

#splitInHalf 
E33 = dcel.getHeById(33)
dcel.splitInHalf(E33)

# slideEdge E36
dcel.slideEdge(E33.twin, 500)

##############################
# test slide edge and cancelslide

e11 = dcel.getHeById(11)
print('slide e11: code should be 1 1')
rec11 = dcel.slideEdge(e11, 100)

e18 = dcel.getHeById(18)
print('slide e18: code should be 2 2')
rec18 = dcel.slideEdge(e18, 100)

e29 = dcel.getHeById(29)
print('slide e29: code should be 1 3')
rec29 = dcel.slideEdge(e29, 100)

e33 = dcel.getHeById(33)
print('slide e33: code should be 3 1')
rec33 = dcel.slideEdge(e33, 100)

e39 = dcel.getHeById(39)
print('slide e39: code should be 3 3')
rec39 = dcel.slideEdge(e39, 100)

dcel.killSlideEdge(rec39)
dcel.killSlideEdge(rec33)
dcel.killSlideEdge(rec29)
dcel.killSlideEdge(rec18)

e11 = dcel.getHeById(11)

edges = dcel.getCycleFrom(e11)
points = [(edge.origin.coord.x, edge.origin.coord.y) for edge in edges if edge.origin]
# vertices = []
# vertices.append((vertice.x, vertice.y))
path = Path(points)
ok = path.contains_points([(e11.origin.coord.x, e11.origin.coord.y), (e11.destination.coord.x, e11.destination.coord.y)])
# testMergeE()

e36 = dcel.getHeById(36)
############################################################
dcel.draw()