import matplotlib.pyplot as plt
import pdb

from ..brush import NodeBrush, EdgeBrush
from ..context import DynamicShow


def test_edgenode():
    with DynamicShow() as ds:
        brush = NodeBrush('nn.input', ds.ax, size='normal')
        ebrush = EdgeBrush('directed', ds.ax, lw=2, color='r')
        node1 = brush >> (0.5, 0.5)
        node1.text('center', 'center')
        node2 = brush >> (2.5, 1.5)
        node2.text('left', 'left')
        brush.style = 'tn.mpo'
        node3 = brush >> (1.0, 2.2)
        node3.text('mpo', 'center', color='w')
        e1 = ebrush >> (node2, node1)
        e1.text('right-directed', 'right')

        ebrush.style = 'undirected'
        e2 = ebrush >> (node2, node3)
        e2.text('top-undirected', 'top')

        brush.style = 'tn.tri'
        node4 = brush >> (2.5, 2.2)
        node4.text('triangle', color='w')
        ebrush.color = 'g'
        ebrush.style = 'arrow'
        e3 = ebrush >> (node4, node3)
        e3.text('green-bottom-arrow', 'bottom')
        brush.style = 'tn.tri_d'
        brush.size = 'tiny'
        ebrush.lw = 1
        node5 = brush >> (1.2, 0.)
        node5.text('triangle-down-right-tiny, lw=1', 'right', color='y')
        e4 = ebrush >> (node3, node5)


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
        edge = EdgeBrush('directed', ds.ax, lw=2.)
        undirected_edge = EdgeBrush('undirected', ds.ax, lw=2.)

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


if __name__ == '__main__':
    test_edgenode()
    # test_tebd()
