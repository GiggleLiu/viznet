import pdb, fire
from viznet import theme, EdgeBrush, DynamicShow, Grid, NodeBrush
import matplotlib.pyplot as plt
import numpy as np
import time

nbrush = NodeBrush("tn.mps", color="#31e0cf")
selfloop = NodeBrush("basic", size="small",zorder=-10)
e2v = NodeBrush("tn.mps", size="tiny", color="r", zorder=2)
edge = EdgeBrush("-", color="#333333", lw=2)
edge2 = EdgeBrush(".", color="#DD7722", lw=2)

class TW(object):
    def origin(self, tp="png"):
        with DynamicShow(figsize=(5,4), filename="origin.%s"%tp) as ds:
            xs = [0,0,-1,1,-2,0,2.0]
            ys = [3,2,1,1,0,0,0.0]
            locs = zip(xs, ys)
            A, B, C, D, E, F, G = [nbrush >> loc for loc in locs]
            for x in ["A", "B", "C", "D", "E", "F", "G"]:
                eval("%s.text('%s')"%(x,x))

            pairs = [(A, B), (B, C), (B, D), (C, E), (C, F), (D, F), (D, G),(E, F), (F, G)]
            edges = [edge >> pair for pair in pairs]

    def mapping(self, tp="gif"):
        with DynamicShow(figsize=(5,4), filename="mapping.%s"%tp) as ds:
            xs = [0,0,-1,1,-2,0,2.0]
            ys = [3,2,1,1,0,0,0.0]
            locs = zip(xs, ys)
            A, B, C, D, E, F, G = [nbrush >> loc for loc in locs]
            for x in ["A", "B", "C", "D", "E", "F", "G"]:
                eval("%s.text('%s')"%(x,x))

            pairs = [(A, B), (B, C), (B, D), (C, E), (C, F), (D, F), (D, G),(E, F), (F, G)]
            edges = [edge >> pair for pair in pairs]

            def share_vertex(pair_i, pair_j):
                return (pair_i[0] in pair_j) or (pair_i[1] in pair_j)

            enodes = []

            def f1():
                enodes[:] = [e2v >> e.position for e in edges]
                return enodes

            def f2():
                Ne = len(pairs)
                els = []
                for i in range(Ne):
                    for j in range(i+1,Ne):
                        if share_vertex(pairs[i], pairs[j]):
                            els.append(edge2 >> (enodes[i], enodes[j]))
                return els

            ds.steps = [f1, f2]

    def mapped(self, tp="png"):
        with DynamicShow(figsize=(5,4), filename="mapped.%s"%tp) as ds:
            xs = [0,0,-1,1,-2,0,2.0]
            ys = [3,2,1,1,0,0,0.0]
            locs = zip(xs, ys, "ABCDEFG")
            A, B, C, D, E, F, G = locs
            pairs = [(A, B), (B, C), (B, D), (C, E), (C, F), (D, F), (D, G),(E, F), (F, G)]

            def share_vertex(pair_i, pair_j):
                return (pair_i[0] in pair_j) or (pair_i[1] in pair_j)

            enodes = []

            def f1():
                for p in pairs:
                    en = e2v >> ((p[0][0]+p[1][0])/2, (p[0][1]+p[1][1])/2)
                    en.text(p[0][2]+p[1][2])
                    enodes.append(en)
                return enodes

            def f2():
                Ne = len(pairs)
                els = []
                for i in range(Ne):
                    for j in range(i+1,Ne):
                        if share_vertex(pairs[i], pairs[j]):
                            els.append(edge2 >> (enodes[i], enodes[j]))
                return els

            f1()
            els = f2()
            pdb.set_trace()
            for e in els:
                e.obj.remove()

    def contract(self, tp="gif"):
        steper = NodeBrush("basic")
        dbl = EdgeBrush('=', lw=2)
        with DynamicShow(figsize=(5,4), filename="contract.%s"%tp) as ds:
            st = steper >> (3, 3)
            t = st.text("")
            xs = [0,0,-1,1,-2,0,2.0]
            ys = [3,2,1,1,0,0,0.0]
            locs = zip(xs, ys)
            nds = [nbrush >> loc for loc in locs]
            A, B, C, D, E, F, G = nds
            for obj,x in zip([A, B, C, D, E, F, G], ["A", "B", "C", "D", "E", "F", "G"]):
                obj.text(x)
                obj.edges = []
                obj.label = x

            pairs = [(A, B), (B, C), (B, D), (C, E), (C, F), (D, F), (D, G),(E, F), (F, G)]
            _pairs = [(A, B), (B, C), (B, D), (C, E), (C, F), (D, F), (D, G),(E, F), (F, G)]
            corder = [0, 2, 6, 5, 8, 1, 4, 7,3]

            edges = []
            for (ip,pair) in enumerate(pairs):
                e = edge >> pair
                e.vertices = pair
                pair[0].edges.append(ip)
                pair[1].edges.append(ip)
                edges.append(e)

            removed_list = []
            sl = []
            def update(i):
                ip = corder[i]
                X, Y = pairs[ip]
                _X, _Y = _pairs[ip]
                st.objs[-1].remove()
                t = st.text(_X.label+_Y.label)
                if pairs[ip] in removed_list:
                    sl[-1].remove()
                    return
                removed_list.append(pairs[ip])
                print(X.label, Y.label)
                res = edges[ip].remove()
                nnode = nbrush >> edges[ip].position
                nnode.edges = []
                nnode.label = X.label+Y.label
                nnode.text(nnode.label)
                if i in [3,5,7]:
                    sl.append(selfloop >> nnode.pin("top"))
                # special cases
                vl = []
                for ie in X.edges + Y.edges:
                    res = edges[ie].remove()
                    for v in edges[ie].vertices:
                        if v not in (X, Y):
                            if v in vl:
                                #e = dbl >> (v, nnode)
                                e = next(filter(lambda e:e.vertices == (v, nnode), edges))
                                e.obj.set_linewidth(e.obj.get_linewidth()+2)
                            else:
                                e = edge >> (v, nnode)
                            nnode.edges.append(ie)
                            e.vertices = (v, nnode)
                            edges[ie]=e
                            print(ie, e.vertices[0].label, e.vertices[1].label)
                            pairs[ie] = e.vertices
                            vl.append(v)
                        try:
                            v.edges.remove(ie)
                        except:
                            pass
                X.remove()
                Y.remove()
            ds.steps = [lambda j=i: update(j) for i in range(len(corder))]


if __name__ == "__main__":
    fire.Fire(TW)
