import numpy as np
import matplotlib.pyplot as plt
import pdb

from ..brush import NodeBrush, EdgeBrush
from ..context import DynamicShow
from ..circuit import QuantumCircuit


def test_edgenode():
    with DynamicShow() as ds:
        brush = NodeBrush('nn.input', ds.ax, size='normal')
        ebrush = EdgeBrush('->-', ds.ax, lw=2, color='r')
        node1 = brush >> (0.5, 0.5)
        node1.text('center', 'center')
        node2 = brush >> (2.5, 1.5)
        node2.text('left', 'left')
        brush.style = 'tn.mpo'
        node3 = brush >> (1.0, 2.2)
        node3.text('mpo', 'center', color='w')
        e1 = ebrush >> (node2, node1)
        e1.text('right-directed', 'right')

        ebrush.style = '-..-'
        e2 = ebrush >> (node2, node3)
        e2.text('top-undirected', 'top')

        brush.style = 'tn.tri'
        node4 = brush >> (2.5, 2.2)
        node4.text('triangle', color='w')
        ebrush.color = 'g'
        ebrush.style = '->-.....->-'
        e3 = ebrush >> (node4, node3)
        e3.text('green-bottom-arrow', 'bottom')
        brush.style = 'tn.tri_d'
        brush.size = 'tiny'
        ebrush.lw = 1
        node5 = brush >> (1.2, 0.)
        node5.text('triangle-down-right-tiny, lw=1', 'right', color='y')
        e4 = ebrush >> (node3, node5)


def test_ghz():
    num_bit = 4
    with DynamicShow() as ds:
        basic = NodeBrush('qc.basic', ds.ax)
        C = NodeBrush('qc.C', ds.ax)
        NOT = NodeBrush('qc.NOT', ds.ax, size='small')
        END = NodeBrush('qc.end', ds.ax)
        M = NodeBrush('qc.measure', ds.ax)
        BOX = NodeBrush('box',ds.ax,size=(0.5,2.0))

        handler = QuantumCircuit(ds.ax, num_bit=4)
        handler.x+=0.5
        handler.gate(basic, 0, 'X')
        for i in range(1,num_bit):
            handler.gate(basic, i, 'H')
        handler.x+=1
        handler.gate((C, NOT), (1,0))
        handler.gate((C, NOT), (3,2))
        handler.x+=0.7
        handler.gate((C, NOT), (2,0))
        handler.x+=0.7
        handler.gate((C, NOT), (3,2))
        handler.x+=1
        for i in range(num_bit):
            handler.gate(basic, i, 'H')
        handler.x+=1
        handler.gate(BOX, (0,1,2,3), '$e^{-iHt}$')
        handler.x+=1
        for i in range(num_bit):
            handler.gate(M, i)
        handler.edge.ls = '='
        handler.x+=0.8
        for i in range(num_bit):
            handler.gate(END, i)

        # text |0>s
        for i in range(num_bit):
            plt.text(-0.4, i, r'$\vert0\rangle_{Q_%d}$'%i,va = 'center', ha='center', fontsize=18)

def test_tebd():
    # remove the edges for nodes
    from ..setting import node_setting
    from .. import theme
    node_setting['lw'] = 1

    with DynamicShow() as ds:
        # define a set of brushes.
        size = 'large'
        mps = NodeBrush('tn.mps', ds.ax, size=size)
        invisible_mps = NodeBrush('invisible', ds.ax, size=size)
        mpo2 = NodeBrush('tn.mpo21', ds.ax, size=size)
        edge = EdgeBrush('->-', ds.ax, lw=2.)
        undirected_edge = EdgeBrush('---', ds.ax, lw=2.)

        mps_list = []
        for i in range(8):
            mps_list.append(mps >> (i, 0))
        mps_list.append(invisible_mps >> (i + 1, 0))

        for layer in range(4):
            # set brush color
            mpo2.color = theme.RED if layer % 2 == 0 else theme.GREEN
            mpo_list = []
            start = layer % 2
            for i, (mps_l, mps_r) in enumerate(zip(mps_list[start::2], mps_list[start + 1::2])):
                mpo_list.append(
                    mpo2 >> (mps_l.position + mps_r.position) / 2. + (0, layer + 1))
                if layer == 0:
                    pin_l = mps_l
                    pin_r = mps_r
                else:
                    pin_l = mpo_list_pre[i].pin('top', align=mps_l)
                    pin_r = mpo_list_pre[i].pin('top', align=mps_r)
                if layer < 2:
                    undirected_edge >> (mps_l, mps_r)
                edge >> (pin_l, mpo_list[-1].pin('bottom', align=mps_l))
                edge >> (pin_r, mpo_list[-1].pin('bottom', align=mps_r))
            mpo_list_pre = mpo_list

def test_pin():
    with DynamicShow() as ds:
        # define a set of brushes.
        size = 'large'
        mpo = NodeBrush('tn.mpo21', ds.ax, size=size)
        mps = NodeBrush('tn.mps', ds.ax, size=size)
        edge1 = EdgeBrush('->', ds.ax, lw=2., color='r')
        edge2 = EdgeBrush('<->', ds.ax, lw=2., color='r')
        n1 = mpo >> (0, 0)
        n2 = mpo >> (2, 2)
        n3 = mps >> (1, 3)
        e1 = edge1 >> (n1, n2.pin(np.pi/4., align=n1))
        edge2 >> (n3.pin(np.pi/2, align=e1), e1.center)


if __name__ == '__main__':
    test_ghz()
    test_edgenode()
    test_pin()
    # test_tebd()
