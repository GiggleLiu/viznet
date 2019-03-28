from viznet import theme, EdgeBrush, DynamicShow, Grid, NodeBrush
import matplotlib.pyplot as plt
import numpy as np

nbrush = NodeBrush("tn.mps", color="#31e0cf")
e2v = NodeBrush("tn.mps", size="tiny", color="r", zorder=2)
edge = EdgeBrush("-", color="#333333", lw=2)
edge2 = EdgeBrush(".", color="#DD7722", lw=2)

def plot_demo():
    with DynamicShow(figsize=(5,4), filename="treewidth.gif") as ds:
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

        ds.frames = [f1, f2]

plot_demo()
