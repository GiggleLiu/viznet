import numpy as np
import matplotlib.pyplot as plt
import pdb

from ..brush import NodeBrush, EdgeBrush, CLinkBrush
from ..edgenode import Pin
from ..context import DynamicShow
from ..circuit import QuantumCircuit
from ..cluster import node_ring


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
        brush.style = 'tn.tri'
        brush.rotate = np.pi
        brush.size = 'tiny'
        ebrush.lw = 1
        node5 = brush >> (1.2, 0.)
        node5.text('triangle-down-right-tiny, lw=1', 'right', color='y')
        e4 = ebrush >> (node3, node5)


def test_ghz():
    num_bit = 4
    handler = QuantumCircuit(num_bit=4)
    basic = NodeBrush('qc.basic')
    C = NodeBrush('qc.C')
    NOT = NodeBrush('qc.NOT', size='small')
    END = NodeBrush('qc.end')
    M = NodeBrush('qc.measure')
    BOX = NodeBrush('qc.box')
    with DynamicShow() as ds:
        handler.x += 0.5
        handler.gate(basic, 0, 'X')
        for i in range(1, num_bit):
            handler.gate(basic, i, 'H')
        handler.x += 1
        handler.gate((C, NOT), (1, 0))
        handler.gate((C, NOT), (3, 2))
        handler.x += 0.7
        handler.gate((C, NOT), (2, 0))
        handler.x += 0.7
        handler.gate((C, NOT), (3, 2))
        handler.x += 1
        for i in range(num_bit):
            handler.gate(basic, i, 'H')
        handler.x += 1
        handler.gate(BOX, (0, 1, 2, 3), '$e^{-iHt}$')
        handler.x += 1
        for i in range(num_bit):
            handler.gate(M, i)
        handler.edge.ls = '='
        handler.x += 0.8
        for i in range(num_bit):
            handler.gate(END, i)

        # text |0>s
        for i in range(num_bit):
            plt.text(-0.4, -i, r'$\vert0\rangle_{Q_%d}$' %
                     i, va='center', ha='center', fontsize=18)


def test_edge():
    edge_list = ['-', '..-', '->--', '<=>', '===->', '->-....-<-']
    clink_list = ['->', '<->', '>.>']
    offsets = [(), (-0.2, 0.2), (0.15, 0.3, -0.3)]
    with DynamicShow(figsize=(8, 6)) as ds:
        for i, style in enumerate(edge_list):
            edge = EdgeBrush(style, ds.ax)
            p1 = Pin((0, -i * 0.1))
            p2 = Pin((1, -i * 0.1))
            ei = edge >> (p1, p2)
            p1.text('"%s"'%style, 'left')
            if i == 0: ei.text('EdgeBrush', 'top')
        for j, (style, offset) in enumerate(zip(clink_list, offsets)):
            p1 = Pin((0, -i * 0.1 - (j+1)*0.3))
            p2 = Pin((1, -i * 0.1 - (j+1)*0.3))
            clink = CLinkBrush(style, color='r', roundness=0.05, offsets=offset)
            ei = clink >> (p1, p2)
            if j == 0: ei.text('CLinkBrush', 'top')
            p1.text('"%s", %s'%(style, str(offset)), 'left')


def test_tebd():
    # remove the edges for nodes
    from ..setting import node_setting
    from .. import theme
    node_setting['lw'] = 1

    with DynamicShow() as ds:
        # define a set of brushes.
        size = 'large'
        mps = NodeBrush('tn.mps', ds.ax, size=0.3)
        invisible_mps = NodeBrush('invisible', ds.ax, size=size)
        mpo2 = NodeBrush('tn.mpo', ds.ax, size=(0.7, 0.25))
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
        mpo = NodeBrush('tn.mpo', ds.ax, size=size)
        mps = NodeBrush('tn.mps', ds.ax, size=size)
        edge1 = EdgeBrush('->', ds.ax, lw=2., color='r')
        edge2 = EdgeBrush('<->', ds.ax, lw=2., color='r')
        n1 = mpo >> (0, 0)
        n2 = mpo >> (2, 2.2)
        n3 = mps >> (1, 3)
        e1 = edge1 >> (n1, n2.pin(5*np.pi / 4., align=n1))
        edge2 >> (n3.pin(np.pi / 2, align=e1), e1.center)


def test_connect():
    edge = EdgeBrush('->', lw=2., color='r')
    with TestShow(grid=(2,3), num_node=2) as ts:
        ax, (n1, n2) = ts.ax((0, 0), num_node = 2, style='tn.mpo')
        edge >> (n1, n2)
        edge >> (n1, (3, 3))

def test_polygon():
    edge = EdgeBrush('->', lw=2., color='r')
    with DynamicShow() as ds:
        path = [(-1,0), (0, -1), (2,2)]
        # node theme can be define as (color, geometry, and inner-geometry) tuple. polygon requires 'path' property.
        geo = NodeBrush(('#981255', 'polygon', 'odot'), roundness=0.2, props={'path':path})
        paths = [[(-1, -1), (0, -1), (0, 1)], [(-1,0), (1, 0)]]

        # another flexible definition of node is lines, it take multiple paths.
        lines = NodeBrush(('#981255', 'lines', 'none'), roundness=0.2, props={'paths':paths})
        g = geo >> (0, 0)
        l = lines >> (1,2)
        edge >> (g, l)

        # when using pin,
        edge >> (g.pin(np.pi/2.), l.pin('left'))
        l.text('left-side', 'left')
        l.text('bottom-side', -np.pi/2.)

def test_grid():
    from ..grid import Grid
    grid = Grid((2.0, 1.2), offset=(2,2))
    brush = NodeBrush('basic')
    edge = EdgeBrush('->', lw=2., color='r')
    box = NodeBrush('box', roundness=0.2, size='large')

    # define an mpo
    mpo = NodeBrush('box', color='g', roundness=0.2)

    brushes = []
    with DynamicShow() as ds:
        for i in range(4):
            for j in range(4):
                brushes.append(brush >> grid[i, j])
        for i in range(15):
            edge >> (brushes[i], brushes[i+1])
        box >> grid[1:2, 1:2]

        # generate two mpos
        A = mpo >> grid[4:5, 0:0]
        B = mpo >> grid[4:5, 2:3]

        # connect left legs.
        edge >> (A.pin('top', align = grid[4, 0]), B.pin('bottom', align = grid[4, 0]))
        edge >> (B.pin('bottom', align = grid[5, 0]), A.pin('top', align = grid[5, 0]))

class TestShow():
    '''
    Dynamic plot context, intended for displaying geometries.
    like removing axes, equal axis, dynamically tune your figure and save it.

    Args:
        figsize (tuple, default=(6,4)): figure size.
        filename (filename, str): filename to store generated figure, if None, it will not save a figure.

    Attributes:
        figsize (tuple, default=(6,4)): figure size.
        filename (filename, str): filename to store generated figure, if None, it will not save a figure.
        ax (Axes): matplotlib Axes instance.

    Examples:
        with DynamicShow() as ds:
            c = Circle([2, 2], radius=1.0)
            ds.ax.add_patch(c)
    '''

    def __init__(self, figsize=(6, 4), filename=None, dpi=300, grid=(1,1), num_node=2):
        self.figsize = figsize
        self.filename = filename
        self.grid = grid
        self.num_node = num_node

    def ax(self, ij, num_node=0, style='basic'):
        ax = plt.subplot(self.gs.__getitem__(ij))
        node_list = node_ring(NodeBrush(style, ax), self.num_node, (0,0), 1.0)
        return ax, node_list

    def __enter__(self):
        plt.ion()
        plt.figure(figsize=self.figsize)
        self.gs = plt.GridSpec(*self.grid)
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if traceback is not None:
            return False
        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()
        if self.filename is not None:
            print('Press `c` to save figure to "%s", `Ctrl+d` to break >>' %
                  self.filename)
            pdb.set_trace()
            plt.savefig(self.filename, dpi=300)
        else:
            pdb.set_trace()

if __name__ == '__main__':
    test_polygon()
    test_pin()
    test_ghz()
    test_grid()
    test_connect()
    test_tebd()
    test_edge()
    test_edgenode()
