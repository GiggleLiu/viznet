import numpy as np
import viznet
def logo1():
    with viznet.DynamicShow(figsize=(4,4), filename='_logo.png') as ds:
        n1 = viznet.NodeBrush('tn.dia', color='#CC3333') >> (0, 0)
        n2 = viznet.NodeBrush('qc.cross') >> (1, 0)
        n3 = viznet.NodeBrush('tn.mpo', size=0.25) >> (1, 1)
        n4 = viznet.NodeBrush('nn.memory') >> (0, 1)
        viznet.EdgeBrush('<.>') >> (n1, n2)
        viznet.EdgeBrush('<.>') >> (n2, n3)
        viznet.EdgeBrush('-<=') >> (n3, n4)
        viznet.EdgeBrush('=>-') >> (n4, n1)

def logo2():
    viznet.setting.node_setting['inner_lw'] = 2
    viznet.setting.node_setting['lw'] = 2
    with viznet.DynamicShow(figsize=(4,4), filename='_logo.png') as ds:
        body = viznet.NodeBrush('tn.dia', size='huge', color='#FF7744') >> (0, 0)
        b1 = viznet.NodeBrush('tn.mpo', size='large', color='#CC3333') >> (0, 0)
        b2 = viznet.NodeBrush('tn.dia', size='small') >> (0, 0)
        n1 = viznet.NodeBrush('qc.cross') >> (1, 1)
        n2 = viznet.NodeBrush('qc.cross') >> (-1, 1)
        n3 = viznet.NodeBrush('qc.cross') >> (-1, -1)
        n4 = viznet.NodeBrush('qc.cross') >> (1, -1)
        viznet.EdgeBrush('=>-', lw=2) >> (body, n1)
        viznet.EdgeBrush('=>-', lw=2) >> (body, n2)
        viznet.EdgeBrush('=>-', lw=2) >> (body, n3)
        viznet.EdgeBrush('=>-', lw=2) >> (body, n4)

if __name__ == '__main__':
    logo2()
