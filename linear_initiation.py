# single loaded starter kit

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

####################################################
# modify it into a house plan

v1 = A
v2 = B
v3 = C
v4 = D


# Housing Unit Parameter?
width = 6000
depth = 3000
rooms = 4

# v1.moveTo(Vector(-1800,0,0))
v2.moveTo(Vector(depth, 0, 0))
v3.moveTo(Vector(depth, width, 0))
v4.moveTo(Vector(0, width, 0))

# divide rooms 
r = 1
if rooms > r:
    e4 = dcel.getHeById(4)
    e2 = dcel.getHeById(2)
    dcel.splitInHalf(e4)
    dcel.splitInHalf(e2)
    dcel.splitFace(e4, e2)
    r = r + 1

    if rooms > r:
        e10 = dcel.getHeById(10)
        e7 = dcel.getHeById(7)
        # e13 = dcel.getHeById(13)
        dcel.splitInHalf(e10)
        dcel.splitInHalf(e7)
        dcel.splitFace(e10, e7)
        r = r + 1

        if rooms > r:
            e11 = dcel.getHeById(11)
            dcel.splitInHalf(e4)
            dcel.splitInHalf(e11)
            dcel.splitFace(e4, e11)
            r = r + 1

            # if rooms > r:
            #     e17 = dcel.getHeById(17)
            #     dcel.splitInHalf(e3)
            #     dcel.splitInHalf(e17)
            #     dcel.splitFace(e3, e17)
            #     r = r + 1

            #     if rooms > r:
            #         e15 = dcel.getHeById(15)
            #         e13 = dcel.getHeById(13)
            #         dcel.splitInHalf(e15)
            #         dcel.splitInHalf(e13)
            #         dcel.splitFace(e13, e15)
            #         r = r + 1

            #         if rooms > r:
            #             e21 = dcel.getHeById(21)
            #             e28 = dcel.getHeById(28)
            #             dcel.splitInHalf(e21)
            #             dcel.splitFace(e21, e28)
            #             r = r + 1

            #             if rooms > r:
            #                 e34 = dcel.getHeById(34)
            #                 dcel.splitInHalf(e1)
            #                 dcel.splitFace(e1, e34)
            #                 r = r + 1
                            
# print(r)

# # function configuration setting:
F2 = dcel.getFaceById(2)
F2.fun = "L"
F3 = dcel.getFaceById(3)
F3.fun = "D"
F4 = dcel.getFaceById(4)
F4.fun = "BR"
F5 = dcel.getFaceById(5)
F5.fun = "K"
# F6 = dcel.getFaceById(6)
# F6.fun = "BA"
# F7 = dcel.getFaceById(7)
# F7.fun = "EH"
# F8 = dcel.getFaceById(8)
# F8.fun = "BL"

# dcel.randomSwapFun()
# dcel.randomSwapFun()
# dcel.randomSwapFun()
# dcel.randomSwapFun()
# dcel.randomSwapFun()

# dcel.draw()
