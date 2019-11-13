import numpy as np
import matplotlib.pyplot as plt
import pdb

from ..brush import NodeBrush, EdgeBrush, CLinkBrush, CurveBrush
from ..edgenode import Pin
from ..context import DynamicShow
from ..circuit import QuantumCircuit
from ..cluster import node_ring

def graphs(tp='pdf'):
    with DynamicShow((8, 2), '_graphs.%s'%tp) as ds:
        nb = NodeBrush('basic', size='tiny', color='k')
        cb = CurveBrush('-', color='k', lw=2)
        loop = NodeBrush("basic", size="small", zorder=-1, lw=2)
        en = NodeBrush("tn.mpo", size=0.05, color='k')

        ax = plt.subplot(141)
        A = nb >> (0,0)
        B = nb >> (0.5,0.5)
        C = nb >> (0,1)
        D = nb >> (-1,1)
        cb.color = 'C0'
        cb >> (A, B, 0.2)
        cb.color = 'C1'
        cb >> (A, C, -0.2)
        cb.color = 'C2'
        cb >> (C, B, -0.2)
        cb.color = 'C3'
        cb >> (B, D, -0.2)
        loop.edgecolor = 'none'
        loop >> (D.position[0], D.position[1] + loop._size)
        plt.text(0, -0.3, "Simple Graph", fontsize=10, va="center", ha="center")
        plt.axis("equal")
        plt.axis("off")

        ax = plt.subplot(142)
        A = nb >> (0,0)
        B = nb >> (0.5,0.5)
        C = nb >> (0,1)
        D = nb >> (-1,1)
        cb.color = 'C0'
        cb >> (A, B, 0.2)
        cb.color = 'C4'
        cb >> (A, B, -0.2)
        cb.color = 'C1'
        cb >> (A, C, -0.2)
        cb.color = 'C2'
        cb >> (C, B, -0.2)
        cb.color = 'C3'
        cb >> (B, D, -0.2)
        loop.edgecolor = 'C5'
        loop >> (D.position[0], D.position[1] + loop._size)
        plt.text(0, -0.3, "Multigraph", fontsize=10, va="center", ha="center")
        plt.axis("equal")
        plt.axis("off")

        ax = plt.subplot(143)
        A = nb >> (0,0)
        B = nb >> (0.5,0.5)
        C = nb >> (0,1)
        D = nb >> (-1,1)
        cb.color = 'C0'
        cb >> (A, B, 0.2)
        cb.color = 'C4'
        cb >> (A, B, -0.2)
        E4 = en >> (-0.1, 0.5)
        cb.color = 'C1'
        cb >> (A, E4, -0.2)
        cb >> (E4, C, -0.2)
        cb.color = 'C2'
        cb >> (C, B, -0.2)
        cb.color = 'C1'
        cb >> (B, E4, -0.2)
        cb >> (E4, D, -0.2)
        cb.color = 'C5'
        E1 = en >> (-0.9, 0.3)
        cb >> (D, E1, 0.2)
        plt.text(0, -0.3, "Hypergraph", fontsize=10, va="center", ha="center")
        plt.axis("equal")
        plt.axis("off")

        ax = plt.subplot(144)
        A = nb >> (0,0)
        B = nb >> (0.5,0.5)
        C = nb >> (0,1)
        D = nb >> (-1,1)
        cb.color = 'C0'
        cb >> (A, B, 0.2)
        cb.color = 'C0'
        cb >> (A, B, -0.2)
        cb.color = 'C1'
        cb >> (A, C, -0.2)
        cb.color = 'C0'
        cb >> (C, B, -0.2)
        cb.color = 'C1'
        cb >> (B, D, -0.2)
        loop.edgecolor = 'C5'
        loop >> (D.position[0], D.position[1] + loop._size)
        plt.text(0, -0.3, "Others", fontsize=10, va="center", ha="center")
        plt.axis("equal")
        plt.axis("off")

if __name__ == "__main__":
    graphs("png")
