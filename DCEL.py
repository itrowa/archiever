from vect import Point, Vector
import string
import numpy as np
import random
from scipy.spatial import ConvexHull
from matplotlib.path import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from itertools import cycle
import copy
import pickle
import networkx as nx

class DCEL:
    """ An double connected edge list object.
    """

    def __init__(self):
        """ Initialize an empty DCEL object. """
        self.vertices = []
        self.halfEdges = []
        self.faces = []
        self.outerFace = self.newFace(fun="OUT")
        self.rg = nx.Graph()

    def newFace(self, fun="CR"):
        f = Face(fun=fun)
        self.faces.append(f)
        return f

    def newVertex(self, coordinates):
        v = Vertex(coordinates)
        self.vertices.append(v)
        return v

    def newHalfEdge(self, origin, face):
        he = HalfEdge(origin, face)
        self.halfEdges.append(he)
        return he

    def rmVertex(self, vertex):
        self.vertices.remove(vertex)

    def rmHalfEdge(self, hf):
        self.halfEdges.remove(hf)

    def newPlan(self):
        """ add new Plan to current dcel obj.
            (recommend use it only after first initialize.)
        """
    def linkFace(self, f1, f2):
        """ Link two faces together (in order to set connection relationship) """
        f1.linkFaceTo(f2)
        f2.linkFaceTo(f1)

    def getMaxConLen(self, face):
        """ get max continuous length for face. """
        edges = self.getCycleFrom(face.incidentEdge)
        pass

    def getCycleFrom(self, e):
        """ Returns an List containing all the HalfEdges 
            in the face incident to e in counter-clockwise order starting from e. 
        """
        cycleEdges = []

        for temp in self.halfEdges:
            if temp == e:
                while True:
                    cycleEdges.append(e)
                    e = e.next
                    if e == temp:
                        break
        return cycleEdges

    def getOutBoundingEdges(self, e):
        """ get all outbounding edges from e.origin. starting from e itself."""
        edges = []

        for temp in self.halfEdges:
            if temp == e:
                while True:
                    # print("e:", e)
                    edges.append(e)
                    e = e.twin.next
                    if temp == e:
                        break
        return edges

    def splitFace(self, e1, e2):
        """ Splits the face incident to e1 and e2 by adding an edge between the origins of e1 and e2. 
            If e1 and e2 are not incident to the same face, or e1 is the next or prev of e2, nothing should
            happen (because the call isn't "legal"). 
            return: newly added face
        """

        # 0 Check weather the call is legal and return if not .
        if e1 == e2 or e1.next == e2 or e2.next == e1 or e1.face != e2.face:
            raise Exception("Cann't perform splitFace operation: edge1 and edge2 \
                should point to the same face and they are not the prev/next to each other.")
            return
        else:
            # 1. Create a new face for the second half of the split. 
            fNew = self.newFace() # check correctness!
            fOld = e2.face

            # 2. Create new half-edges for the splitting edge:
            newEdge = self.newHalfEdge(e1.origin, fOld)
            newReverseEdge = self.newHalfEdge(e2.origin, fNew)

            newEdge.twin = newReverseEdge
            newReverseEdge.twin = newEdge

            # 3. Insert your new half-edges into the cyclic lists: 
                # some helper pointers
            e1p = e1.prev
            e2p = e2.prev

                # set prev/next pointers
            e1p.next = newEdge
            newEdge.prev = e1p
            newEdge.next = e2
            e2.prev = newEdge

            e2p.next = newReverseEdge
            newReverseEdge.prev = e2p
            newReverseEdge.next = e1
            e1.prev = newReverseEdge

            # 4. Make sure that all the half-edges point to the right face
            newReverseEdgeCycle = self.getCycleFrom(newReverseEdge)
            for he in newReverseEdgeCycle:
                he.face = fNew

            newEdgeCycle = self.getCycleFrom(newEdge)
            for he in newEdgeCycle:
                he.face = fOld

            # 5. Make sure that each face correctly refers to an incident half-edge
            fOld.incidentEdge = newEdge;
            fNew.incidentEdge = newReverseEdge;
            return fNew

    def killEdge(self, e):
        """ kill edge e with its origin
        """
        # save some pointers
        en = e.next
        ep = e.prev
        et = e.twin
        etp = e.twin.prev
        etn = e.twin.next
        ed = e.twin.origin
        eo = e.origin
        ef = e.face
        etf = e.twin.face
        edges = self.getOutBoundingEdges(e)

        # set prev/next pointers
        en.prev = ep
        ep.next = en
        etp.next = etn
        etn.prev = etp

        # set edge origin
        for _ in edges:
            _.origin = ed
        etn.origin = ed

        # set face incident edge
        ef.incidentEdge = en
        etf.incidentEdge = etp

        # delete vertex, edges
        self.rmHalfEdge(e)
        self.rmHalfEdge(e.twin)
        self.rmVertex(eo)

    def splitByT(self, e, t):
        """ split edge e in by parameter t and return newly added edge.
            t = 0 means  newly added verted at e.origin.
            e's destination remains not change, but e.origin points to newly added vertex
        """
        if t < 0 or t > 1:
            raise Exception("Cannot Split Edge ", e,  " with t=", t, ": t Should Satisfy 0<=t<=1.")
        else:
            # just run splitInPlace()
            nv = self.splitInPlace(e)

            # and move newly created vertex into midPt position
            p1 = e.origin.coord
            p2 = e.twin.origin.coord
            midPt = p1.eval_2pts(p2, t)
            nv.moveTo(midPt)

            return e.prev

    def splitInHalf(self, e):
        """ split edge e in half and return newly added vertex.
            e's destination remains not change, but e.origin points to newly added vertex
        """
        # just run splitInPlace()
        nv = self.splitInPlace(e)

        # and move newly created vertex into midPt position
        p1 = e.origin.coord
        p2 = e.twin.origin.coord
        midPt = p1.mid_point(p2)
        nv.moveTo(midPt)

        return nv

    def splitInPlace(self, e):
        """ split edge e with newly added vertex at e.origin and return newly added vertex. """

        # p1 = e.origin.coord
        # p2 = e.twin.origin.coord
        newPt = Vector(e.origin.coord.x, e.origin.coord.y, e.origin.coord.z)
        midV = self.newVertex(newPt)

        # 2. Create the two new half-edges
        e1 = self.newHalfEdge(e.origin, e.face)
        e2 = self.newHalfEdge(midV, e.twin.face)

        # 3. Set HalfEdge pointers

        # Set edge origin vertex
        e.origin = midV

        # Set edge next/prev pointers
        ep = e.prev
        etn = e.twin.next

        ep.next = e1
        e1.next = e
        e1.prev = ep
        e.prev = e1
        e.twin.next = e2
        e2.prev = e.twin
        e2.next = etn
        etn.prev = e2

        # Set edge twin pointers
        e1.twin = e2
        e2.twin = e1

        # Set edge face pointers
        e1.face = e.face
        e2.face = e.twin.face

        return midV

    def draw(self, draw=True, filename="default.png"):
        """ Draw All the Verts, Faces and Edges for diagnostics. """
        # draw points
        fig = plt.figure(figsize=(8,8), dpi=96)
        ax = fig.add_subplot(111)
        cycol = cycle('bgrcmyw') #@caution:python3 only
        colormap = {
            "CR": "#233D4D",
            "BR": "#7899D4",
            "K": "#71D16C",
            "L": "#F7CE5B",
            "D": "#21B719",
            "BA": "#7272AB",
            "EH": "#DDDDDD",
            "ST": "#1F0812",
            "BL": "#8E443D",
            "EQ": "#777777",
            "OUT": "#EEEEEE"
        }

        # draw vertices
        for v in self.vertices:
            i,j = v.coord.x, v.coord.y
            plt.plot(i, j, 'ro')
            plt.annotate("V"+str(v.id), xy=(i+5, j+5))

        # draw faces
        for f in self.faces:
            if f != self.outerFace:
                edges = self.getCycleFrom(f.incidentEdge)
                if edges:
                    points = []
                    codes = []
                    for he in edges:
                        # draw sth
                        # annoPt = Vector() annoPt
                        points.append((he.origin.coord.x, he.origin.coord.y))
                        codes.append(Path.LINETO)

                    points.append(tuple(points[0]))
                    codes.append(Path.CLOSEPOLY)
                    codes[0] = Path.MOVETO

                    path = Path(points, codes)
                    # print (points)
                    # print (codes)

                    patch = patches.PathPatch(path, facecolor=colormap[f.fun], lw=2)
                    ax.add_patch(patch)
                    # annotation
                    annoPt = self.faceCenterPoint(f)
                    plt.annotate("F" + str(f.id) + ":" + str(f.fun), color="#ee8d18", xy=(annoPt.x, annoPt.y))

        # draw edges
        for edge in self.halfEdges:
            # draw it! 
            plt.plot([edge.origin.coord.x, edge.twin.origin.coord.x], 
                     [edge.origin.coord.y, edge.twin.origin.coord.y],
                     linestyle=':', color='g', lw=0.5)
            anp = edge.getAnnotationPoint()
            plt.annotate("E"+str(edge.id), xy=(anp.x-100, anp.y))

        plt.axes().set_aspect('equal')
        ax.set_xlim(-4000, 10000)
        ax.set_ylim(-4000, 10000)

        if draw == True:
            plt.show()
        else:
            plt.savefig(filename)

    def faceArea(self, f):
        """ Compute area of a specific face f. """
        points = self.facePoints(f)
        area = self.polyArea2D(points)
        return area

    def faceConvexHullArea(self, f):
        """ COmpute the area of the convex hull of specific face f. """
        # @note: hull.area is no equal to this one. which is correct?
        points = self.facePoints(f)
        hull = ConvexHull(points)
        return self.polyArea2D(points[hull.vertices])

    def facePoints(self, f):
        """ return a ndarray points list for a face f. """
        edges = self.getCycleFrom(f.incidentEdge)
        if edges:
            pts = []
            for e in edges:
                pts.append([e.origin.coord.x, e.origin.coord.y])
            return np.array(pts)
        else:
            raise Exception("Cannot get facePoints: Face has no Edges")

    def faceCenterPoint(self, f):
        """ get center Point for face f. """
        pts = self.facePoints(f)
        # print(pts[:,0])
        # print(pts[:,1])
        tpt = pts.sum(axis=0) # sum over all x and all y and get total pt

        # calculate averge and return
        return Vector(tpt[0]/(pts[:,0].size), tpt[1]/(pts[:,1].size), 0)

    def polyArea2D(self, pts):
        """ compute the poly area of pts. pts is 2d nd array. """
        lines = np.hstack([pts,np.roll(pts,-1,axis=0)])
        area = 0.5*abs(sum(x1*y2-x2*y1 for x1,y1,x2,y2 in lines))
        return area

    def moveTo(self, vector, relative=False):
        """ move all vertices to a vector. """
        for v in self.vertices:
            v.moveTo(vector, relative=relative)

    def slideEdge(self, e, dist): # test Ok!
        """ poposal slide a edge in dcel by a dist. dist is positive 
            means slide inward to its incident face. dist should be positive! """

        # note: 刚开始，在此函数内判断dist是否合适，这样会来了一个问题，那就是有时候这个函数其实并不工作。这就会
        # 它的逆操作带来了困难， 所以应该100%执行，要不直接raise Exception.

        # note: 第二个问题是，此函数的逆操作要判断此函数是执行的哪一种情况。刚开始，我在dcel的整个对象上添加了一些类属性，
        # 但是这就带来了迭代的问题……更好的办法是，让这个函数返回操作的信息，让调用它的代码去接收这些信息，为逆操作做准备.

        if dist < 0:
            raise Exception("Cannot slide Edge ", e, " with distance ", dist, ", dist should be non-negative.")
        # elif e.length() == 0 or e.prev.length() <= dist or e.next.length() <= dist:
        #     # when e.prev or e.next has a length less than moving distance, sliding will 
        #     # create inappropirate consequence, so we should avoid this case.
        #     print("I will not slide Edge ", e, " bacause remaining distance is not enough or ", e, "'s length is too small.")
        #     return False
        else:
            eVector = e.vector() 
            eVP = eVector.perpendicular_2d().multiply(abs(dist))
            # print("eVector:", eVector)
            # print("eVP:", eVP)

            # starting from destination side of e is there any edge parallel to e?
            temp = e.next
            edclear = True
            while temp != e.twin:
                if temp.vector().parallel(eVector):
                    # need to add a new vertex
                    edclear = False
                    break 
                else:
                    temp = temp.twin.next
            # print("ED clear?", edclear)

             # starting from origin side of e is there any edge parallel to e?
            temp = e.twin.next
            eoclear = True
            while temp != e:
                if temp.vector().parallel(eVector):
                    eoclear = False
                    break
                else:
                    temp = temp.twin.next     
            # print("EO clear?", eoclear)

            rec = {}
            rec['e'] = e
            rec['ed'] = copy.deepcopy(e.twin.origin.coord)
            rec['eo'] = copy.deepcopy(e.origin.coord)
            rec['edop'] = self.splitEDest(e, edclear, eVector, eVP)
            rec['eoop'] = self.splitEOrigin(e, eoclear, eVector, eVP)

            return rec


    def splitEDest(self, e, clear, vector, direction):
        """ Do not use this standalone.
            move e's destination point according to e's original vector, and direction vector.
            return OPCode.
        """

        # 有和它平行的边
        if clear == False: 
        # print("DEBUG: e and e.next len is: ", e.length(), e.next.length())

            # e.next 和moving 之前的e平行
            # print("e.next para to e?",  e.next.vector().parallel(vector))
            # print("e, e.next, e.next.vector(), evector", e, e.next, e.next.vector(), vector)
            if e.next.vector().parallel(vector):
            # if e.next.isPerpendicularTo(e):
                # save operation code
                vsp = self.splitInPlace(e.twin)
                code = 2

            else: # e.next和 moving 之前的e垂直

                # make split
                vsp = self.splitInPlace(e.next)

                # save pointers
                en = e.next
                enn = e.next.next
                etp = e.twin.prev

                # set edge prev/next pointers
                etp.next = en
                en.prev = etp
                en.next = e.twin
                e.twin.prev = en
                e.next = enn
                enn.prev = e

                # set edge origin
                e.twin.origin = vsp

                # set edge incident face
                en.face = e.twin.face

                code = 3

            # move vsp
            vsp.moveTo(direction, relative=True)

        # 没有和它平行的边        
        else:
            e.twin.origin.moveTo(direction, relative=True)
            code = 1

        return code


    def splitEOrigin(self, e, clear, vector, direction): #@todo: check correct
        """ move e's origin point according to e's oroginal vector and direction vector.
        """

        # 有和e平行的边
        if clear == False:
            # e.prev 平行于e moving 之前的vector
            # print("e.prev para to e?",  e.prev.vector().parallel(vector))
            if e.prev.vector().parallel(vector):
            # if e.prev.isPerpendicularTo(e):
                # save operation code
                vsp = self.splitInPlace(e)
                code = 2

            # e.prev 垂直于e moving 之前的vector
            else:
                # make split
                vsp = self.splitInPlace(e.prev.twin)  

                # save pointers
                etn = e.twin.next
                ep = e.prev
                epp = e.prev.prev
                # print("3.1. etn, ep, epp = ", etn, ep, epp)

                # set edge prev/next  小心指针在设置中被改变！！
                epp.next = e
                e.prev = epp
                e.twin.next = ep
                ep.prev = e.twin
                ep.next = etn
                etn.prev = ep

                # set edge origin
                e.origin = vsp

                # set edge incident face
                ep.face = e.twin.face         

                code = 3

            # move split point
            vsp.moveTo(direction, relative=True)

        # 没有和e平行的边
        else:        
            # print("3 e", e, "edge list is:", self.getCycleFrom(e))
            e.origin.moveTo(direction, relative=True)
            code = 1

        return code

    def killSlideEdge(self, rec):
        """ kill last operation by slideEdge(). by recovery information returned by slideEdge()"""
        if not rec:
            raise Exception("Cannot Recover From Last Slide: rec is None.")
        else:
            self.killSplitEDest(rec)
            self.killSplitEOrigin(rec)

    def killSplitEDest(self, rec):
        e = rec['e']
        if rec['edop'] == 0:
            pass # last time no slide at all
        elif rec['edop'] == 1:
            e.twin.origin.moveTo(rec['ed']) 
        elif rec['edop'] == 2:
            self.killEdge(e.next)
        elif rec['edop'] == 3:
            # create some pointers
            en = e.next
            etp = e.twin.prev
            etpp = e.twin.prev.prev
            etpo = e.twin.prev.origin

            # set edge prev/next pointers
            e.next = etp
            etp.prev = e
            etp.next = en
            en.prev = etp
            e.twin.prev = etpp
            etpp.next = e.twin

            # set edge origin:
            e.twin.origin = etpo

            # set edges incident face
            etp.face = e.face

            # set face incident edge
            e.twin.face.incidentEdge = e.twin

            # kill remaining edges and vertex
            self.killEdge(etp.twin)
        else:
            raise Exception("kill e's Destination Sliding failed: Unknown Op Code:", rec['edop'])

    def killSplitEOrigin(self, rec):
        e = rec['e']
        if rec['eoop'] == 0:
            pass
        elif rec['eoop'] == 1:
            e.origin.moveTo(rec['eo'])
        elif rec['eoop'] == 2:
            self.killEdge(e.twin.next)
        elif rec['eoop'] == 3:
            # create some pointers
            ep = e.prev
            etn = e.twin.next
            etnn = e.twin.next.next
            etnno = e.twin.next.next.origin

            # set edge prev/next pointers
            ep.next = etn
            etn.prev = ep
            etn.next = e
            e.prev = etn
            e.twin.next = etnn
            etnn.prev = e.twin

            # set edge origin:
            e.origin = etnno

            # set edges incident face
            etn.face = e.face

            # set face incident edge
            e.twin.face.incidentEdge = e.twin

            # kill remaining edges and vertex
            self.killEdge(etn)
        else:
            raise Exception("kill e's Origin Sliding failed: Unknown Op Code:", rec['eoop'])

    def mergeE(self, e):
        """ merge e's destination and origin. see file!
        """
        # 需要保证e的detination he origin处都没有和e平行的边!
        # @todo : 添加测试e两边是否有和e平行的边的代码？

        enl = e.next.length()
        epl = e.prev.length()

        if abs(enl - epl) < 10:
            # print("enl = epl!")
            self.mED(e)
            self.mEO(e)
        elif enl > epl:
            # print("enl > epl!")
            e.destination.moveTo(e.vector().rotate_ccw_90().multiply(epl), relative=True)
            self.mEO(e)
        elif epl > enl:
            # print("epl > enl!")
            e.origin.moveTo(e.vector().rotate_ccw_90().multiply(enl), relative=True)
            self.mED(e)
        else:
            raise Exception("cannot perform merge: e.next.length() or e.prev.length() has issues.")

        # merge完成后 检查e的左右两边是否有和e平行的边 以方便杀边.
        if e.next.isParallelTo(e) and e.prev.isParallelTo(e):
            self.killEdge(e)
        elif e.next.isParallelTo(e):
            self.killEdge(e.twin)
        elif e.prev.isParallelTo(e):
            self.killEdge(e)
        else:
            pass
            # raise Exception("cannot perform merge: after meo and med, somethin has happend.")

    def mED(self, e):
        """ merge e's destination vertex to e.next.destination. 
        """
        # e'dest 必须没有与之平行的边！@todo 稍后添加测试条件.

        # case 1
        if e.next.twin is e.twin.prev:
            self.killEdge(e.next)

        # case 2
        else:
            # some pointers
            en = e.next
            enn = e.next.next
            et = e.twin
            etp = e.twin.prev
            end = e.next.destination

            # update prev/next
            e.next = enn
            enn.prev = e

            etp.next = en
            en.prev = etp
            en.next = et
            et.prev = en

            # update edge origin
            et.origin = end

            # update edge incident face
            en.face = et.face

            # update face incident edge
            e.face.incidentEdge = e

            # kill en
            self.killEdge(en)

    def mEO(self, e):
        """ merge e's origin vertex to 
        """
        # e'origin 必须没有与之平行的边！@todo 稍后添加测试条件.

        # case 1
        if e.twin.next is e.prev.twin:
            self.killEdge(e.twin.next)
        # case 2
        else:
            # some pointers
            et = e.twin
            etn = e.twin.next
            ep = e.prev
            epp = e.prev.prev
            epo = e.prev.origin

            # update prev/next
            e.prev = epp
            epp.next = e

            et.next = ep
            ep.prev = et
            ep.next = etn
            etn.prev = ep

            # update edge origin
            e.origin = epo

            # update edge incident face
            ep.face = et.face

            # update face incident edge
            e.face.incidentEdge = e

            # kill ep and its origin
            self.killEdge(ep)

    def proposalMergeE(self, e):
        # 判断e是否适合merge，并进行merge.
        # @todo: 判断条件应该加上: e的destination 和origin侧都没有和e平行的边.

        # 如果e.next是e逆时针转了90度的方向 或者 e.prev是e顺时针转了90度的方向，那就
        # 可以执行mergeE()
        edclear = e.vector().rotate_ccw_90().parallels(e.next.vector())
        eoclear = e.vector().rotate_cw_90().parallels(e.prev.vector())
        if edclear or eoclear:
            self.mergeE(e)
            # print("proposalMergeE(): Done!")
        else:
            pass
            # print("proposalMergeE(): Constraints not Satisfied!")

    def swapFun(self, f1, f2):
        f1.fun, f2.fun = f2.fun, f1.fun
        f1.req, f2.req = f2.req, f1.req      

    def isInFace(self, e, boundary):
        """ is e's origin and destination vertex in boundary path? """
        # edges = self.getCycleFrom(e)
        # points = [(edge.origin.coord.x, edge.origin.coord.y) for edge in edges if edge.origin]
        # path = Path(points)
        path = boundary
        ok = path.contains_points([(e.origin.coord.x, e.origin.coord.y), (e.destination.coord.x, e.destination.coord.y)])
        if ok[0] and ok[1]:
            return True
        else:
            return False

    def getPathBoundary(self, e):
        """ get path boundary for e's cycle edges. """
        edges = self.getCycleFrom(e)
        points = [(edge.origin.coord.x, edge.origin.coord.y) for edge in edges if edge.origin]
        path = Path(points)
        return path

    def isValidSlide(self, e, boundary):
        """ is the slide is valid slide? """
        if e.face == self.outerFace:
            return True
        else:
            return self.isInFace(e, boundary)

    def proposalSlideEdge(self, e=None):
        """ proposal slide An Edge by a random distance. 
            if no edge ref is given, it will randomly choose an edge to slide. 
        """
        # 1. get random sliding dist, from 300 to 2000
        ds = list(range(500, 1500, 100))
        dist = random.choice(ds)

        # 2. choose edge to slide
        if not e:
            edge = random.choice(self.halfEdges)
        else:
            edge = e

        # ( get boundary before slide)
        original_boundary = self.getPathBoundary(edge)

        # 3. slide selected edge
        rec = self.slideEdge(edge, dist)

        # 4. check if slided result is not valid:
        if not self.isValidSlide(edge, original_boundary):
            self.killSlideEdge(rec)
            # print("no edge slided! ")
            return None
        else:
            return rec

        # maybe neeed merge? 
        # ...

    def proposalExplore(self):
        """ proposal Expolore plan state by randomly split and slide An Edge.
        """
        # get random t's(edge split parameter, from 0.1 to 0.9) choice
        ts = [x*0.1 for x in range(0, 10)] # @caution @todo this list comprehension has floating round issues, but seems work ok.
        t = random.choice(ts)
        ne = self.splitByT(random.choice(self.halfEdges), t)

        #  查看拆分结果 如果拆分后两段edge的长度太小，则取消拆分，随机slide一条edge
        # 如果拆分后两段edge长度合适，就slide新添加的那条edge

        if ne.length() < 300 or ne.next.length() < 300:
            self.killEdge(ne.twin)
            rec = self.proposalSlideEdge()
        else:
            rec = self.proposalSlideEdge(ne)

        return rec

    def randomSplitSlide(self):
        """ randomly split and slide An Edge. after that, merge E if remaining room is small. 
            Return rec dict if Success. 
            if not success, return None
            not success的情况：slide以后，边跑到了原来face的外面.
        """
        def isInFace(e):
            """ is e's origin and destination vertex in e.face ? """
            edges = self.getCycleFrom(e)
            points = [(edge.origin.coord.x, edge.origin.coord.y) for edge in edges if edge.origin]
            path = Path(points)
            ok = path.contains_points([(e.origin.coord.x, e.origin.coord.y), (e.destination.coord.x, e.destination.coord.y)])
            if ok[0] and ok[1]:
                return True
            else:
                return False

        # get random t's(edge split parameter, from 0.1 to 0.9) choice
        ts = [x*0.1 for x in range(0, 10)] # @caution @todo this list comprehension has floating round issues, but seems work ok.
        t = random.choice(ts)

        # get  random sliding dist 
        ds = list(range(0, 2001, 100))
        dist = random.choice(ds)

        # get random edge to slide
        edge = random.choice(self.halfEdges)

        ne = self.splitByT(edge, t)
        # newEdge = edge.prev

        #  查看拆分结果 如果拆分后两段edge的长度太小，则取消拆分，然后slide原来的edge:
        if ne.length() < 300 or edge.length() < 300:
            # print ("I will not creat Edge ", ne, ", because newly created Edge caused a short length. proceed to slide")
            self.killEdge(ne.twin)
            rec = self.slideEdge(edge, dist)

            if not self.isInFace(edge):
                self.killSlideEdge(rec)
                print("randomSplitSlide(): ", ne, " created but cancelled, ", edge, " slided but cancelled." )
                return None
            else:
                if edge.next.length() < 300 or edge.prev.length() < 300:
                    self.proposalMergeE(edge)
                    print("randomSplitSlide(): ", ne, " created but cancelled, ", edge, " slided and merged." )
                else:
                    print("randomSplitSlide(): ", ne, " created but cancelled, ", edge, " slided." )
                    return rec

        # if split success perform slide on newlly added edge
        else: 
            rec = self.slideEdge(ne, dist)

            # 检查slide后的效果是不是满意，如果不满意则取消这次slide, 和边的分裂
            if not self.isInFace(ne):
                self.killSlideEdge(rec)
                self.killEdge(ne.twin)
                print("randomSplitSlide(): ", ne, " created, slideded but cancelled." )
            else:
                if ne.next.length() < 400 or ne.prev.length() < 400:
                    self.proposalMergeE(ne)
                    print("randomSplitSlide(): ", ne, " created, slideded, and merged." )
                else:
                    print("randomSplitSlide(): ", ne, " created and slideded." )
                rec['ne'] = ne
                return rec

    def killRandomSplitSlide(self, rec):
        """ kill randomSplitSlide() by its rec dict. """
        if not rec:
            print("killRandomSplitSlide(): nothinng to kill.")
            return 
        elif 'ne' in rec:
            # 上一次 randomSplitSlide创建了新边并且slide了它.
            print("killRandomSplitSlide(): ", rec['e'], "'s slide cancelled, ", rec['ne'], " killed.")
            self.killSlideEdge(rec)
            self.killEdge(rec['ne'].twin)
        else:
            # 上一次 randomSplitSlide没有创建新边但slide了.
            print("killRandomSplitSlide(): ", rec['e'], "'s slide cancelled,")
            self.killSlideEdge(rec)

    def randomSwapFun(self):
        """ randomly swap two face's function for stochastic layout change.
            return a tuple of two faces' reference
        """

        # retrieve 2 unique elements
        faces = random.sample( [f for f in self.faces if f != self.outerFace] , 2)
        # print(faces)
        f1 = faces[0]
        f2 = faces[1]

        # # saving swap record
        # self.lastSwap = [f1, f2]

        # print ("I will swap ", f1, " and ", f2, "...")
        # print("f1 and f2 fun:", f1.fun, f2.fun)
        f1.fun, f2.fun = f2.fun, f1.fun
        f1.req, f2.req = f2.req, f1.req
        # print("randomSwapFun(): Now ", f1," and ", f2, )
        self.updateFacesAdj()

        return (f1, f2)

        # self.lastSwap = None
        # self.lastCreatedEdge = None

    def killRandomSwapFun(self, rec):
        f1 = rec[0]
        f2 = rec[1]
        print ("I will cancel swap ", f1, " and ", f2, "...")
        f1.fun, f2.fun = f2.fun, f1.fun
        f1.req, f2.req = f2.req, f1.req
        print("Now ", f1," and ", f2, " fun:", f1.fun, f2.fun)

    def updateFacesAdj(self):
        # re-set faces functional connections
        for f in self.faces:
            f.adj = set()
            edges = self.getCycleFrom(f.incidentEdge)
            for e in edges:
                f.adj.add(e.twin.face)

    def getHeById(self, id):
        for he in self.halfEdges:
            if he.id == id: 
                return he

    def getVertexById(self, id):
        for v in self.vertices:
            if v.id == id: 
                return v

    def getFaceById(self, id):
        for f in self.faces:
            if f.id == id: 
                return f

    def set_reqs(self):
        """ assgin all the relation graph nodes to dcel's faces. """

        # 将self.rg这个功能要求图的每一个节点绑定到dcel的face上.方法是，当一个面的fun属性和
        # 在rg node的中的属性相等，就绑定这两个对象.
        # @note: 不是所有的dcel face都会创建和FaceReq对象的绑定.
        remaining_reqs = list(reqs)
        for f in self.faces:
            # create room req binding
            # print("for ", f, "fun: ", f.fun)
            for r in reqs:
                if f.fun == r.fun:
                    f.req = r
                    remaining_reqs.remove(r)
                    # print("created bindng to: ", r)
                    # print("ramaining reqs:", remaining_reqs)
                    break
            # print("f.req: ",f, f.req)

class HalfEdge:
    cnt = 1
    def __init__(self, origin, face):
        """ Origin: an Vertex."""
        self.origin = origin
        self.twin = None
        self.next = None
        self.prev = None
        self.face = face
        origin.outgoingEdge = self
        self.id = HalfEdge.cnt
        HalfEdge.cnt += 1

    def __repr__(self):
        name = "HE"
        return name + str(self.id) + "(" + str(self.origin.coord) + ") -> " + str(self.twin.origin.coord) + ")"

    @property
    def destination(self):
        return self.twin.origin

    # @property
    def length(self):
        """ compute the length of this HalfEdge. """
        # @todo improve length zero case? @caution: check
        l = self.twin.origin.coord.substract(self.origin.coord).length()
        if l == 0:
            return random.uniform(0.0001, 0.01)
        else:
            return l

    def vector(self):
        """ compute its directional unit vector. """
        # @caution: always check length before compute vector!
        # @todo : check if vector length = 0
        if self.length() == 0:
            return (Vector(random.uniform(0.01, 0.09), random.uniform(0.01, 0.09), 0))
        else:
            return self.twin.origin.coord.substract(self.origin.coord).normalize()

    def getMidPt(self):
        """ get mid pt for this edge. """
        # print(self.origin)
        midPt = self.origin.coord.mid_point(self.twin.origin.coord)
        return midPt

    def isPerpendicularTo(self, he):
        """ is self is perpendicular to half edge he? (just 2D)"""
        # print(self.vector(), he.vector())
        return self.vector().is_perpendicular_to(he.vector())

    def isParallelTo(self, he):
        """ is self is parallel to half edge he? (just 2d) """
        return self.vector().parallel(he.vector())

    def isParallelToS(self, he):
        """ is self is parallel to half edge he (strictly)? (just 2d)
            # note: strictly means: negative direction edges are not parallel.
            return self.vector().parallel(he.vector())
        """ 
        return self.vector().parallels(he.vector())

    def getAnnotationPoint(self):
        """ computes annotation point for plt. """
        # midPt = self.origin.coord.mid_point(self.twin.origin.coord)
        midPt = self.getMidPt()
        # print("self.vector ",self.vector())
        # @caution: zero division error when the edge has 0 length!
        directionV = self.vector()#.sum(Vector(random.uniform(0.001, 0.009), random.uniform(0.001, 0.009), 0))
        # print("dv ",directionV)
        annoPt = midPt.sum(directionV.perpendicular_2d().multiply(200)) 
        return annoPt

class Vertex:
    cnt = 1

    def __init__(self, coordinates):
        """ Coordinates is a vector obj."""
        self.coord = coordinates
        self.outgoingEdge = None
        self.id = Vertex.cnt
        Vertex.cnt += 1

    def __repr__(self):
        name = "V"
        return name + str(self.id) + ": " + str(self.coord)

    def moveTo(self, coordinates, relative=False):
        """ move this vertex into a new coordinates. 
            coordinates: Vector obj.
        """
        if relative == False:
            self.coord = coordinates
        else:
            self.coord = self.coord.sum(coordinates)

class Face:
    cnt = 1
    funs = set(["CR", "BR", "K", "L", "D", "BA", "EH", "ST", "BL", "EQ", "OUT"])
    #           走廊  卧室 厨房 客厅  就餐  厕所  门厅  储藏  阳台   设备  外部
    def __init__(self, fun="CR"):
        """ it'a face; it's a node. """
        self.incidentEdge = None

        # Think Face as Graph Nodes!
        self.adj = set() # adjoint faces (in graph).
        self.fun = fun
        self.id = Face.cnt
        Face.cnt += 1
        self.req = None  # pointer to a design req.

    def __repr__(self):
        name = "F"
        return name + str(self.id) + ": " + str(self.fun) + " with " + str(self.req)

    def linkFaceTo(self, face):
        """ link a face to another face. 
            try not to use this function standalone.
        """
        self.adj.add(face)

    def setType(self, fun):
        """ set function type for this face. """
        self.fun = fun



def DCELTest():
    """ testing with previously lab graph. """
    dcel = DCEL()
    # Create the six vertices A--F: 
    A = dcel.newVertex(Vector(-300, -150, 0))
    B = dcel.newVertex(Vector(0, -150, 0))
    C = dcel.newVertex(Vector(300, -150, 0));
    D = dcel.newVertex(Vector(300, 150, 0));
    E = dcel.newVertex(Vector(0, 150, 0));
    F = dcel.newVertex(Vector(-300, 150, 0));

    # Create a face for the inner face; Note: the outer face is dcel.outerFace
    f = dcel.newFace()

    # Create the six half-edges for inner face
    AB = dcel.newHalfEdge(A, f);
    BC = dcel.newHalfEdge(B, f);
    CD = dcel.newHalfEdge(C, f);
    DE = dcel.newHalfEdge(D, f);
    EF = dcel.newHalfEdge(E, f);
    FA = dcel.newHalfEdge(F, f);

    # Make sure you set an incident half edge for f: 
    f.incidentEdge = AB;

    # Set up the next/prev pointers correctly for the face: 
    AB.next = BC 
    BC.prev = AB
    BC.next = CD 
    CD.prev = BC
    CD.next = DE 
    DE.prev = CD
    DE.next = EF 
    EF.prev = DE
    EF.next = FA 
    FA.prev = EF
    FA.next = AB 
    AB.prev = FA

    # Create the six half-edges for the outer face
    AF = dcel.newHalfEdge(A, dcel.outerFace);
    FE = dcel.newHalfEdge(F, dcel.outerFace);
    ED = dcel.newHalfEdge(E, dcel.outerFace);
    DC = dcel.newHalfEdge(D, dcel.outerFace);
    CB = dcel.newHalfEdge(C, dcel.outerFace);
    BA = dcel.newHalfEdge(B, dcel.outerFace);

    # Make sure you set an incident half-edge for the outer face: 
    dcel.outerFace.incidentEdge = AF;

    # Set up the next/prev pointers correctly for the face: 
    AF.next = FE
    FE.prev = AF
    FE.next = ED
    ED.prev = FE
    ED.next = DC
    DC.prev = ED
    DC.next = CB
    CB.prev = DC
    CB.next = BA
    BA.prev = CB
    BA.next = AF
    AF.prev = BA

    # Set twins between the six inner and six outer half-edges
    AB.twin = BA
    BA.twin = AB
    BC.twin = CB
    CB.twin = BC
    CD.twin = DC
    DC.twin = CD
    DE.twin = ED
    ED.twin = DE
    EF.twin = FE
    FE.twin = EF
    FA.twin = AF
    AF.twin = FA

    dcel.getCycleFrom(AB)
    dcel.getCycleFrom(BC)
    dcel.getCycleFrom(CD)

    f1 = dcel.splitFace(BC, EF)
    f2 = dcel.splitFace(BC, DE)
    dcel.splitInHalf(EF);
    f3 = dcel.splitFace(AB.next, AB.next.next.next)
    f4 = dcel.splitFace(AB.next.next, AB)
    dcel.splitInHalf(AB.next)
    dcel.splitInHalf(AB.prev)
    f5 = dcel.splitFace(AB.next.next, AB.prev)
    dcel.splitInHalf(AB.next)
    dcel.splitInHalf(AB.prev)
    f6 = dcel.splitFace(AB.next.next, AB.prev)

    # A.moveTo(Vector(50,50,0), relative=True)

    # test facePoints, face area, face convex hull area
    print(dcel.facePoints(f1))
    print(dcel.faceArea(f1))
    print(dcel.faceConvexHullArea(f1))

    # Set adjacent information for faces

    dcel.draw()

def SlidingTest():
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

    ##########o#
    # resize
    A.moveTo(Vector(-1800,0,0))
    B.moveTo(Vector(5900,0,0))
    C.moveTo(Vector(5900,8000,0))
    D.moveTo(Vector(-1800,8000,0))

    ############
    # create 田 shape

    # move these original points
    # B.moveTo(Vector(500,0,0))
    # C.moveTo(Vector(500,500,0))
    # D.moveTo(Vector(0,500,0))

    # split into four grids


    # I = dcel.splitInHalf(EB.prev)
    # G = dcel.splitInHalf(FD.next)
    # H = dcel.splitInHalf(EB.next)
    # f3 = dcel.splitFace(EB.prev, EB.next.next)
    # f4 = dcel.splitFace(EB.prev.twin.next, FD.next.next)

    #################
    # test sliding edge

    # the starting edge for sliding is EB.next.next. (eDestClearance = False, eOriginClearance=True)
    # the following contains many cases for different test sliding condition:
    # dcel.slideEdge(EB.next.next, 100)
    # dcel.slideEdge(EB.next.next, 50)
    # dcel.slideEdge(EB.next.next.twin, 100)
    # dcel.slideEdge(EB.twin, 100)
    # dcel.slideEdge(EB.next.twin, 100)
    # dcel.slideEdge(EB.next.next, 50)
    # dcel.slideEdge(EB.prev.prev, 50)
    # dcel.slideEdge(EB.prev.prev.twin, 50)
    # dcel.slideEdge(EB.prev.twin, 50)
    # dcel.slideEdge(EB.next.next.next.next.twin, 50)

    # E17=dcel.getHeById(17)
    # print("--------------E17----------------")
    # print("Dest:", E17.twin.origin.coord)
    # print("Orig", E17.origin.coord)
    # print("midPt:", E17.origin.coord.mid_point(E17.twin.origin.coord))
    # print("Vector:", E17.vector())
    # print("Vector(Pepen):", E17.vector().perpendicular_2d())
    # print("Vector(Pepen*5):", E17.vector().perpendicular_2d().multiply(5))
    # # print("Anno(Now):",E17.origin.coord.mid_point(E17.twin.origin.coord) (E17.vector().perpendicular_2d().multiply(5)))

    # print("AnnoPt:", E17.getAnnotationPoint())

    #     # midPt = self.origin.coord.mid_point(self.twin.origin.coord)
    #     # mitPt = midPt.sum(self.vector().perpendicular_2d().multiply(5)) 

    # E18=dcel.getHeById(18)
    # print("--------------E18----------------")
    # print("Dest:", E18.twin.origin.coord)
    # print("Orig", E18.origin.coord)
    # print("midPt:", E17.origin.coord.mid_point(E17.twin.origin.coord))
    # print("Vector:", E18.vector())
    # print("Vector(Pepen):", E18.vector().perpendicular_2d())
    # print("Vector(Pepen*5):", E18.vector().perpendicular_2d().multiply(5))
    # print("AnnoPt:", E18.getAnnotationPoint())
    dcel.draw()

def MiscTest():
    """ misc function test."""
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

    # Set twins between the six inner and six outer half-edges
    AB.twin = BA
    BA.twin = AB
    BC.twin = CB
    CB.twin = BC
    CD.twin = DC
    DC.twin = CD
    DA.twin = AD
    AD.twin = DA

    ############
    # haha = dcel.splitInPlace(AB)
    # haha.moveTo(Vector(20,20,0), relative=True)
    print(AB.isPerpendicularTo(BC))
    dcel.draw()

def centerPtTest():
    AnnoPt = Vector(0,0,0)
    points= [(0,0), (10,0), (10,10), (0,10)]

    for pt in points:
        AnnoPt.x += pt[0]
        AnnoPt.y += pt[1]
    AnnoPt.x = AnnoPt.x / len(points)
    AnnoPt.y = AnnoPt.y / len(points)
    print(AnnoPt)


if __name__ == "__main__":
    # a = Vertex(Vector(400, 150, 0))
    # a.moveTo(Vector(0,-100,0), relative=True)
    # DCELTest()
    SlidingTest()
