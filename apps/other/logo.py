import numpy as np
from numpy.random import randint, randn, choice, random
import viznet
from scipy.sparse.csgraph import minimum_spanning_tree
def logo1():
    with viznet.DynamicShow(figsize=(4,4), filename='_logo1.png') as ds:
        n1 = viznet.NodeBrush('tn.dia', color='#CC3333') >> (0, 0)
        n2 = viznet.NodeBrush('qc.cross') >> (1, 0)
        n3 = viznet.NodeBrush('tn.mpo', size=0.25) >> (1, 1)
        n4 = viznet.NodeBrush('nn.memory') >> (0, 1)
        viznet.EdgeBrush('<.>') >> (n1, n2)
        viznet.EdgeBrush('<.>') >> (n2, n3)
        viznet.EdgeBrush('-<=') >> (n3, n4)
        viznet.EdgeBrush('=>-') >> (n4, n1)

def logo2():
    viznet.setting.node_setting['inner_lw'] = 0
    viznet.setting.node_setting['lw'] = 0
    with viznet.DynamicShow(figsize=(4,4), filename='_logo2.png') as ds:
        body = viznet.NodeBrush('tn.dia', size=1, color='#44CCFF') >> (0, 0)
        b1 = viznet.NodeBrush('tn.mpo', size='large', color='#5588CC') >> (0, 0)
        b2 = viznet.NodeBrush('tn.dia', size='small', color='#331133') >> (0, 0)
        viznet.setting.node_setting['inner_lw'] = 2
        l=1.0
        brush = viznet.NodeBrush('qc.cross', rotate=np.pi/4.)
        n1 = brush >> (l, l)
        n2 = brush >> (-l, l)
        n3 = brush >> (-l, -l)
        n4 = brush >> (l, -l)
        viznet.EdgeBrush('.>-', lw=2) >> (body, n1)
        viznet.EdgeBrush('.>-', lw=2) >> (body, n2)
        viznet.EdgeBrush('.>-', lw=2) >> (body, n3)
        viznet.EdgeBrush('.>-', lw=2) >> (body, n4)

def logo3():
    viznet.setting.node_setting['inner_lw'] = 0
    viznet.setting.node_setting['lw'] = 0
    npoint = 60
    nedge = 50
    angle = random(npoint)*2*np.pi
    #r = np.exp(randn(npoint)*0.4)
    r = np.sqrt(randn(npoint))
    xy = np.array([r*np.cos(angle), r*np.sin(angle)]).T
    #xy = randn(npoint, 2)*0.5
    with viznet.DynamicShow(figsize=(4,4), filename='_logo3.png') as ds:
        #body = viznet.NodeBrush('tn.mps', size='huge', color='#AACCFF') >> (0, 0)
        dot = viznet.NodeBrush('tn.mps', size='tiny')
        node_list = []
        for i, p in enumerate(xy):
            dot.color = random(3)*0.5+0.5
            dot.zorder = 100+i*2
            dot.size = 0.05+0.08*random()
            node_list.append(dot >> p)
        dis_mat = np.linalg.norm(xy-xy[:,None,:], axis=-1)
        tree = minimum_spanning_tree(dis_mat).tocoo()
        for i, j in zip(tree.row, tree.col):
            n1,n2=node_list[i],node_list[j]
            viznet.EdgeBrush(choice(['.>.', '.>.']), lw=1, color=random([3])*0.4, zorder=(n1.obj.zorder+n2.obj.zorder)/2) >> (n1,n2)
        #for i in range(nedge):
        #    n1, n2 =choice(node_list),choice(node_list)
         #   viznet.EdgeBrush(choice(['.>.', '->-']), lw=1, color=random([3])*0.4, zorder=(n1.obj.zorder+n2.obj.zorder)/2) >> (n1,n2)


def logo4(partly):
    viznet.setting.node_setting['inner_lw'] = 0
    viznet.setting.node_setting['lw'] = 2
    with viznet.DynamicShow(figsize=(4,4), filename='_logo4.svg') as ds:
        dot = viznet.NodeBrush('art.rbox', size=0.5)
        tall = 5
        xs = np.zeros(tall)
        ys = np.arange(tall)
        dot.color = '#333333'
        for x, y in zip(xs, ys):
            dot >> (x,y)

        xs = [-1, 0, 1]
        ys = (tall-2)*np.ones(3)
        dot.color = '#FF9933'
        for x, y in zip(xs, ys):
            dot >> (x,y)

        xs = [1, 2, 2, 2]
        ys = [2, 2, 1, 0]
        dot.color = '#333333'
        for x, y in zip(xs, ys):
            dot >> (x,y)

        if not partly:
            x0=5
            xs = x0 + np.arange(3)
            ys = [3, 3, 3]
            dot.color = '#333333'
            for x, y in zip(xs, ys):
                dot >> (x,y)

            ys = [1, 1, 1]
            dot.color = '#333333'
            for x, y in zip(xs, ys):
                dot >> (x,y)

            x0+=5
            xs = np.ones(tall)*x0
            ys = np.arange(tall)
            dot.color = '#333333'
            for x, y in zip(xs, ys):
                dot >> (x,y)
     
if __name__ == '__main__':
    #logo4(True)
    #logo2()
    logo3()
