import matplotlib.pyplot as plt
import pdb

from ..brush import NodeBrush, EdgeBrush
from ..context import DynamicShow

def test_edgenode():
    with DynamicShow() as ds:
        brush = NodeBrush('nn.input', ds.ax, size='normal')
        ebrush = EdgeBrush('directed', ds.ax, lw=2, color='r')
        node1 = brush >> (0.5,0.5)
        node1.text('center', 'center')
        node2 = brush >> (2.5,1.5)
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
        ebrush.lw = 1
        node5 = brush >> (1.2, 0.)
        node5.text('triangle-down-right, lw=1', 'right', color='y')
        e4 = ebrush >> (node3, node5)


if __name__ == '__main__':
    test_edgenode()
