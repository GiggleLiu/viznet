import copy
from viznet import EdgeBrush, DynamicShow, Grid, NodeBrush, CLinkBrush, QuantumCircuit, Pin, setting
import matplotlib.pyplot as plt
import numpy as np

# themes
GRAY = '#D4D4D4'
RED = '#F0201C'
BLUE = '#1072B6'
GREEN = '#00B122'
YELLOW = '#FF9223'
LAKE = '#00A79B'

VIOLET = '#6611CC'
PINK = '#DF678C'
GRASS = '#CCF381'

LW = 3
setting.node_setting['lw'] = LW
setting.node_setting['inner_lw'] = LW

blue = NodeBrush('basic', size=0.2, color=BLUE)
yellow = NodeBrush('basic', size=0.2, color=YELLOW)
red = NodeBrush('basic', size=0.2, color=RED)
green = NodeBrush('basic', size=0.2, color=GREEN)
lake = NodeBrush('basic', size=0.2, color=LAKE)
gray = NodeBrush('basic', size=0.25, color=GRAY)

violet = NodeBrush('basic', size=0.2, color=VIOLET)
pink = NodeBrush('basic', size=0.2, color=PINK)
grass = NodeBrush('basic', size=0.2, color=GRASS)
# edges
edge = EdgeBrush('-', lw=LW)

def plot_ctmrg():
    with DynamicShow(figsize=(6,4), filename="_ctmrg.png") as pl:
        grid = Grid(([1.0,0],[0.5,0.8]))
        box = NodeBrush('box', size=(0.5,0.2), color="#333333", roundness=0.1, edgecolor="#333333")

        redline = EdgeBrush('-', lw=LW, color="#000000", zorder=100)
        blueline = EdgeBrush('-', lw=LW, color="#999999", zorder=-2)
        iedge = copy.copy(edge)
        iedge.zorder= -1

        def ket(isbra=False):
            X2 = 2
            X1 = 1
            Y = 1
            E1 = red >> grid[-X1, Y]
            E3 = red >> grid[-X1, -Y]
            E4 = red >> grid[X1, -Y]
            E6 = red >> grid[X1, Y]
            E2 = red >> grid[-X2, 0]
            E5 = red >> grid[X2, 0]
            ES = [E1, E2, E3, E4, E5, E6]
            C1 = blue >> grid[-X2, Y]
            C2 = blue >> grid[-X2, -Y]
            C4 = blue >> grid[X2, Y]
            C3 = blue >> grid[X2, -Y]

            dYa = 0.3*(1 if isbra else -1)
            bl = copy.copy(grass)
            A1 = bl >> grid[-X1, 0] + [0, dYa]
            A2 = bl >> grid[X1, 0] + [0, dYa]
            
            QUEUE = [E1,C1, E2,C2, E3, E4, C3, E5, C4, E6]
            NQ = 10
            for i in range(NQ):
                iedge >> (QUEUE[i], QUEUE[(i+1)%NQ])
                
            eg = redline if isbra else blueline
            eg >> (E2, A1)
            eg >> (E1, A1)
            eg >> (E3, A1)
            eg >> (E4, A2)
            eg >> (E5, A2)
            eg >> (E6, A2)
            eg >> (A1, A2)
            return A1, A2, ES

        A1, A2, ES = ket(True)
        A1_, A2_, ES_ = ket()
        c = box >> grid[0,0]
        c.text("$\hat{H}$", fontsize=16, color='w')
        redline >> (c, A1)
        blueline >> (c, A1_)
        redline >> (c, A2)
        blueline >> (c, A2_)
        plt.axis("equal")
        plt.axis("off")
        plt.tight_layout()


if __name__ == '__main__':
    plot_ctmrg()
