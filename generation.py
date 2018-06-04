from DCEL import *
from tools import findcaller
from layout1 import dcel
import networkx as nx
import math
import copy
import random
from sys import setrecursionlimit

setrecursionlimit(102400)

# m = {
#     "BR": 25,
#     "K": 8,
#     "L": 20,
#     "D": 10,
#     "BA": 3,
#     "EH": 3,
#     "BL": 4,
# }


class FaceReq:
    """ A FaceReq obj Indicates Design goal for a DCEL Face. """
    def __init__(self, fun, area, direct_sunlight=True):
        # self.w = w
        # self.d = d
        self.area = area
        self.fun = fun
        # optional characteristics
        self.ds = direct_sunlight
        self.enclosure = None

    def __repr__(self):
        return "<FaceReq " + str(self.fun) + " " + str(self.area) + " sqm>"

# Create face reqs:


r1 = FaceReq("BR", 250000000)
r2 = FaceReq("K",   80000000)
r3 = FaceReq("L",  240000000)
r4 = FaceReq("D",  150000000)
r5 = FaceReq("BA",  30000000)
r6 = FaceReq("EH",  30000000, direct_sunlight=False)
r7 = FaceReq("BL",  4000000)

# r1 = FaceReq("BR", 25000000)
# r2 = FaceReq("K",   8000000)
# r3 = FaceReq("L",  24000000)
# r4 = FaceReq("D",  15000000)


# req_list = [r1, r2, r3, r4, r5, r6, r7]
req_list = [r1, r2, r3, r4]

# Add face reqs to dcel.rg:

dcel.rg.add_nodes_from([r1, r2, r3, r4])
dcel.rg.add_edge(r3,r1)
dcel.rg.add_edge(r3,r6)
dcel.rg.add_edge(r3,r2)
dcel.rg.add_edge(r3,r7)
dcel.rg.add_edge(r3,r5)
dcel.rg.add_edge(r3,r4)
dcel.rg.add_edge(r2,r4)

def set_reqs(dcel, reqs):
    """ assign a list of FaceReq **reqs** to dcel's faces. """

    # 创建dcel中每个面和reqs列表中obj的绑定。方法是，当一个面的fun属性和
    # 在reqs的obj中的属性相等，就绑定这两个对象.
    # @caution: 不是所有的dcel face都会创建和FaceReq对象的绑定.
    remaining_reqs = list(reqs)
    for f in dcel.faces:
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

costlog = []
cclog = []
dclog = []
sclog = []
oplog = []
slidelog = []
acceptlog = []
indexlog = []
tsquarelog = []

def compute_cost(x):
    """ compute current plan state's cost function. """
    # kcc=5000000
    kcc = 7000000
    kdc = 0.5
    ksc = 1000000

    cc = kcc*connection_cost(x)
    dc = kdc*dimension_cost(x)
    sc = ksc*shape_cost(x)

    # cost = cc + dc + sc
    cost = dc + cc 
 
    costlog.append(cost)
    cclog.append(cc)
    dclog.append(dc)
    sclog.append(sc)
    # print("----- COST -----")
    # print("COST:", cost)
    # print("CC:", cc)
    # print("DC:", dc)
    # print("SC:", sc)
    return cost

def connection_cost(x):
    """ 计算所有房间连通性的代价函数 
        rg: face req对象的图.
    """
    cc = 0
    # 遍历每一个有设计要求的面 如果这个面 在goal中的连通性没有反映在它实际的连通性中，则加分数加1
    for f in x.faces:
        if f.req:
            # f在当前状态下指向的所有其它的边 都必须出现在f的设计要求中

            # 1. 创建当前状态下f的所有邻接req对象集合。方法是从f.adj中找到所有的face.req对象，并过滤掉None对象
            current_req_set = set([face.req for face in f.adj])
            current_req_set = set([e for e in current_req_set if e is not None])

            # 2. 创建设计要求rg(req graph)中, f的req的所有邻接req的对象集合.
            rg_req_set = set(x.rg.neighbors(f.req))

            # DEBUG INFORMATION
            # print('------- for ', f, " ", f.fun, " ----------")
            # print('f.adj:', f.adj)
            # print('current req sets:', current_req_set)
            # print('rg_req_set:', rg_req_set)

            if rg_req_set <= current_req_set:
                pass
                # print("requirement for face ", f, " satisfied. ")
            else:
                # print("requirement for face ", f, " Not satisfied. ")
                cc += 1
    # print("connection cost: ", cc)
    return cc

def dimension_cost(x):
    # 计算每个房间的指定面积和当前面积的差异.
    dc = 0
    for f in x.faces:
        pass
        if f.req:
        # 如果该房间的面积已经被指定:
            # print("calc Face ", f, "'s area:")
            # print(f, "'s Area is ", x.faceArea(f), "while req area is ", f.req.area)
            adiff = abs(x.faceArea(f) - f.req.area)
            dc += adiff
        else:
            pass
    # print("dimension cost: ", dc)
    return dc

def shape_cost(x):
    # 形状缺陷
    edgecnt = 0
    for f in x.faces:
        if f.fun == "CR" or f.fun == "EH" or f.fun == "L":
            # 针对走廊、玄关和客厅等不计算形状缺陷
            pass
        else:
            edges = x.getCycleFrom(f.incidentEdge)
            # print("edge for ", f, "is", len(edges))
            edgecnt += len(edges)
    # print("shape cost: ", edgecnt)
    return edgecnt

def test_connection_cost():
    """ 计算connection_cost测试.
    """
    print("connection cost:", connection_cost(dcel, rg))

def displayVoidFace(x):
    faces = [f for f in x.faces if not f.incidentEdge]
    if faces:
        print("!!!!", faces, "is Void!!")

# @findcaller
def saveState(x):
    with open ('x.pkl', 'wb') as handle:
        pickle.dump(x, handle, pickle.HIGHEST_PROTOCOL)

def loadState():
    with open ('x.pkl', 'rb') as handle:
        x_prev = pickle.load(handle)
    return x_prev


# beta=0.000004
def generate(x, step, beta=0.0000000003):
    # global rg

    # initial cost
    cost = compute_cost(x)
    for _ in range(step):
          # step = 1
        print("++++++++++++ iteration ", _,  " ++++++++++++++++")
        # print("############## OLD COST: #############")
        # print("COST: ", cost)

        saveState(x)

        # stochastic optimization
        # op = random.choice(list(range(1,4,1)))
        # oplog.append(op)
        # if op == 1:
            # x.proposalExplore()
        # elif op == 2:
            # x.proposalSlideEdge()
        # elif op == 3:
            # x.randomSwapFun()

        # x.proposalSlideEdge()
        success = x.proposalExplore()
        if success:
            slidelog.append(10)
        else:
            slidelog.append(5)
        x.randomSwapFun()

        totalsquare = sum([dcel.faceArea(f) for f in dcel.faces])
        # print("############## TOTAL SQUARE ############")
        tsquarelog.append(totalsquare)

        # print("############## NEW COST: #############")
        cost_ = compute_cost(x)
        delta_cost = cost_ - cost
        # print("DELTA COST: ", delta_cost)

        if delta_cost <= 0:
            # accept new state
            acceptlog.append(10)
            cost = cost_
            # print("STATE CHANGE ACCEPTED!")
        else:
            # accept by a probability
            p = math.exp(beta*(-delta_cost))
            indexlog.append(beta*(-delta_cost))
            # print("STATE CHANGE ACCP BY P:", p)
            ran = random.random()
            # print("RANDOM NUM :", ran)
            if ran > p:
                # print("STATE CHANGE ACCEPTED!")
                cost = cost_
                acceptlog.append(10)
            else:
                # cancel slide and swap
                # print("STATE CHANGE REJECTED!")
                x = loadState()
                # print("DEBUG: IS? ", rgold is rg)
                acceptlog.append(5)

        # x.draw(draw=False, filename=str(_)+".png")

###########################################
## run and visualizing
###########################################

# update faces adj list
dcel.updateFacesAdj()

# bind req_list to dcel.
set_reqs(dcel, req_list)

generate(dcel, 5000, beta=0.0000000018)

# drawing cost
fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

# ax.set_ylim(0,10)
# plt.bar(costlog, color='k', height=1, alpha=0.7, linestyle='--', label='cost')
ax1.plot(cclog, color='y', linestyle=':', label='connection cost')
ax1.plot(dclog, color='k', linestyle=':', label='dimension cost')
# ax1.plot(sclog, color='g', label='shape cost')
ax1.plot(costlog, color='r', alpha=0.7, linestyle='--', label='cost')
ax1.legend()

ax2.scatter(list(range(0, len(indexlog))), indexlog, s=1, color='y', label='-beta*delta_cost')
# ax2.scatter(indexlog, color='y', label='index log')
ax2.legend()

ax3.scatter(list(range(0, len(slidelog))), slidelog, s=0.1, color='y', label='slide success?')
ax3.legend()
# ax3.scatter(acceptlog, color='y', label='accept log')

# ax4.scatter(list(range(0, len(oplog))), oplog, s=0.1, color='y', label='op log')
ax4.plot(tsquarelog, color='y', label='total square')
ax4.plot(dclog, color='k', linestyle=':', label='dimension cost')
ax4.legend()

t10 = acceptlog.count(10)
t5 = acceptlog.count(5)
print("accept/dec ratio: ", t10 / t5)

s10 = slidelog.count(10)
s5 = slidelog.count(5)
print("slide succ/fail ratio: ", s10 / s5)

# top1 = oplog.count(1)
# top2 = oplog.count(2)
# top3 = oplog.count(3)
# topsum = top1 + top2 + top3
# print("op1/op2/op3: ", top1/topsum, ":", top2/topsum, ":", top3/topsum)

# dcel.draw()