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
A.moveTo(Vector(-1300,0,0))
B.moveTo(Vector(5300,0,0))
C.moveTo(Vector(5300,7000,0))
D.moveTo(Vector(-1300,7000,0))

E3 = dcel.getHeById(3)

#creat vertex 5 and move vertex 5
V5 = dcel.splitInPlace(E3)
V5.moveTo(Vector(1000,7000,0))

# slideEdge E9
E9 = dcel.getHeById(9)
dcel.slideEdge(E9.twin, 900)
dcel.slideEdge(E9.twin, 800)
dcel.slideEdge(E9.twin, 1000)
dcel.slideEdge(E9.twin, 300)

#creat vertex 7 and move vertex 7
E2 = dcel.getHeById(2)
V7 = dcel.splitInPlace(E2)
V7.moveTo(Vector(5300,7000,0))

# splitFace E2 E3
dcel.splitFace(E3, E2)

#splitInHalf 
E1 = dcel.getHeById(1)
dcel.splitInHalf(E1)

#creat vertex 9 and move vertex 9
E16 = dcel.getHeById(16)
V9 = dcel.splitInPlace(E16)
V9.moveTo(Vector(2000,7000,0))

# splitFace E16 E1
E1 = dcel.getHeById(1)
dcel.splitFace(E16, E1)

#creat vertex 10 and move vertex 10
V10 = dcel.splitInPlace(E2)
V10.moveTo(Vector(5300,8500,0))

#creat vertex 11 and move vertex 11
E12 = dcel.getHeById(12)
V11 = dcel.splitInPlace(E12)
V11.moveTo(Vector(1000,8500,0))

# splitFace E2 E12
dcel.splitFace(E12, E2)

#creat vertex 12 and move vertex 12
E28 = dcel.getHeById(28)
V12 = dcel.splitInPlace(E28)
V12.moveTo(Vector(2500,8500,0))

#creat vertex 13 and move vertex 13
E9 = dcel.getHeById(9)
V13 = dcel.splitInPlace(E9)
V13.moveTo(Vector(2500,10000,0))

# splitFace E9 E30
E30 = dcel.getHeById(30)
dcel.splitFace(E9, E30)

#creat vertex 14 and move vertex 14
E29 = dcel.getHeById(29)
V14 = dcel.splitInPlace(E29)
V14.moveTo(Vector(3500,8500,0))

#creat vertex 15 and move vertex 15
E20 = dcel.getHeById(20)
V15 = dcel.splitInPlace(E20)
V15.moveTo(Vector(3500,7000,0))

# splitFace E29 E20
dcel.splitFace(E29, E20)

#creat vertex 16 and move vertex 16
E13 = dcel.getHeById(13)
V16 = dcel.splitInPlace(E13)
V16.moveTo(Vector(5300,3000,0))

#creat vertex 17 and move vertex 17
E21 = dcel.getHeById(21)
V17 = dcel.splitInPlace(E21)
V17.moveTo(Vector(2000,3000,0))

# splitFace E13 E21
dcel.splitFace(E13, E21)

#creat vertex 18 and move vertex 18
V18 = dcel.splitInPlace(E13)
V18.moveTo(Vector(5300,4000,0))

#creat vertex 19 and move vertex 19
E43 = dcel.getHeById(43)
V19 = dcel.splitInPlace(E43)
V19.moveTo(Vector(2000,4000,0))

# splitFace E13 E43
dcel.splitFace(E13, E43)

# slideEdge E50
E50 = dcel.getHeById(50)
dcel.slideEdge(E50, 500)

# slideEdge E18
E18 = dcel.getHeById(18)
dcel.slideEdge(E18, 1000)

#creat vertex 22 and move vertex 22
E4 = dcel.getHeById(4)
V22 = dcel.splitInPlace(E4)
V22.moveTo(Vector(-1300,0,0))

# splitFace E4 E22
E22 = dcel.getHeById(22)
dcel.splitFace(E4, E22)

dcel.draw() 