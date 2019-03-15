import numpy as np
import matplotlib.pyplot as plt
import viznet
from viznet import NodeBrush, EdgeBrush, Pin, DynamicShow

RED = '#FF2200'
BLUE = '#333333'
YELLOW= '#BBBBBB'
viznet.setting.node_setting["inner_lw"] = 3
topc = NodeBrush('qc.cross', color=RED, size=0.1, lw=0, zorder=101)
leaf = NodeBrush('basic', color=BLUE, size='tiny', lw=0, edgecolor=BLUE)
base = NodeBrush('basic', color=YELLOW, size='normal', lw=4)
hedge = EdgeBrush('-', lw=5, color=BLUE, zorder=-1, solid_capstyle='round')
vedge = EdgeBrush('-', lw=3, color=RED, zorder=100)

dz = 0.6

def grow(brush, nodes, dr, angle, vbar, size):
    """grow one more layer."""
    nnodes = []
    brush.size = size
    for node in nodes:
        x, y =node.position
        angle0 = np.angle(x+1j*y)
        for nangle in [angle/2 + angle0, -angle/2 + angle0]:
            nx, ny = x+dr*np.cos(nangle), y+dr*np.sin(nangle)
            brush.rotate = nangle+np.pi+np.pi/6
            nnode = brush >> (nx, ny)
            nnodes.append(nnode)
            hedge >> (nnode, node)
            if vbar:
                topnode = topc >> (nx, ny+dz)
                vedge >> (topnode.position, nnode.position)
    return nnodes


def mera():
    with DynamicShow((8, 6), filename='_mera.png') as ds:
        initial = base >> (0, 0.001)
        pin1 = topc >> (-0.1, dz)
        pin2 = topc >> (0.1, dz)
        vedge >> (pin1, Pin([-0.1, 0]))
        vedge >> (pin2, Pin([0.1, 0]))
        nodes = [initial]
        for angle, dr, size in zip([np.pi, np.pi*0.9, np.pi*0.7, 0.4*np.pi], [0.9, 1.0, 0.8, 0.8], [0.3, 0.25, 0.2, 0.15]):
            nodes = grow(base, nodes, dr=dr, angle=angle, vbar=True, size=size)
        grow(leaf, nodes, dr=0.6, angle=0.4*np.pi, vbar=False, size=topc.size)

if __name__ == "__main__":
    mera()
