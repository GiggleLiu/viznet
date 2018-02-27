import numpy as np
import viznet

facecolor = '#BB99FF'
leg_length = 0.2
mpo_offset = 0.4
ldots_span = 1.7
dy = 0.9
edge = viznet.EdgeBrush('-')
dot = viznet.NodeBrush('pin')
hbar = viznet.NodeBrush('tn.mpo21', color=facecolor)
mpo = viznet.NodeBrush('tn.mpo', color=facecolor)
invis = viznet.NodeBrush('invisible')
invis_mini = viznet.NodeBrush('invisible', size='small')

def leg(obj, loc, offset=(0,0)):
    target = obj.pin(loc) + offset
    pin = obj.pin(loc, align=target)
    edge >> (pin, target)

def connect_ldots(node1, node2):
    center = 0.5*(node1.center + node2.center)
    inter = invis >> center.position
    inter.text('$\ldots$', fontsize=18)
    edge >> (node1, inter)
    edge >> (inter, node2)

class Gradient():
    def fig1(self, ext='pdf'):
        with viznet.DynamicShow(figsize=(3,2), filename='fig1.%s'%ext) as ds:
            mpo2 = hbar >> (0.5, 0)
            leg(mpo2, 'left', (-leg_length, 0))
            leg(mpo2, 'right', (leg_length, 0))
            for i in range(2):
                node = invis >> (i, -dy)
                edge >> (mpo2.pin('bottom', align=node), node)

    def fig2(self, ext='pdf'):
        nrow, ncol = 2, 3
        nodes = np.zeros([nrow, ncol], dtype='O')
        with viznet.DynamicShow(figsize=(5,3), filename='fig2.%s'%ext) as ds:
            for i in range(nrow):
                for j in range(ncol):
                    nodes[i, j] = mpo >> (j*ldots_span, i)

            # horizontal lines
            for i in range(nrow):
                for j in range(ncol-1):
                    connect_ldots(nodes[i, j], nodes[i, j+1])

            # vertical lines
            for j in range(ncol):
                for i in range(nrow-1):
                    edge >> (nodes[i,j], nodes[i+1, j])

    def fig3(self, ext='pdf'):
        node_list = []
        dxs = [0, ldots_span, 1, 1, 1, ldots_span]
        xs = np.cumsum(dxs)
        with viznet.DynamicShow(figsize=(6,3), filename='fig3.%s'%ext) as ds:
            for i, x in enumerate(xs):
                if i == 2 or i==3:
                    brush = invis
                else:
                    brush = mpo
                node_list.append(brush >> (x, 0))

            # horizontal lines
            connect_ldots(node_list[0], node_list[1])
            connect_ldots(node_list[4], node_list[5])
            edge >> (node_list[1], node_list[2])
            edge >> (node_list[3], node_list[4])

            # vertical lines
            for node in node_list:
                leg(node, 'bottom', offset=(0, -leg_length))

    def fig4(self, ext='pdf'):
        node_list = []
        node_list2 = []
        dxs = [0, ldots_span, 1, 1, 1, ldots_span]
        xs = np.cumsum(dxs)
        with viznet.DynamicShow(figsize=(6,3), filename='fig4.%s'%ext) as ds:
            for i, x in enumerate(xs):
                if i == 2 or i==3:
                    brush = invis
                else:
                    brush = mpo
                node_list.append(brush >> (x, 0))
                if i == 2:
                    mpo2 = hbar >> ((xs[2]+xs[3])/2., -dy)
                    node_list2.append(mpo2)
                elif i == 3:
                    node_list2.append(mpo2)
                else:
                    node_list2.append(mpo >> (x, -dy))

            # horizontal lines
            for nlist in [node_list, node_list2]:
                connect_ldots(nlist[0], nlist[1])
                connect_ldots(nlist[4], nlist[5])
                edge >> (nlist[1], nlist[2])
                edge >> (nlist[3], nlist[4])

            # vertical lines
            for node, node2 in zip(node_list, node_list2):
                edge >> (node, node2.pin('top', align=node))


    def fig5(self, ext='pdf'):
        # the matric of positions
        dxs = [0, 0.5, ldots_span, 1]
        xs = np.cumsum(dxs)
        dys = [0, 0.7, 0.7]
        ys = -np.cumsum(dys)
        nodes = np.zeros([len(xs), len(ys)], dtype='O')

        with viznet.DynamicShow(figsize=(6,3), filename='fig5.%s'%ext) as ds:
            for i, x in enumerate(xs):
                if x==0:
                    brush = dot
                else:
                    brush = mpo
                for j, y in enumerate(ys):
                    if j==1 and brush is not dot:
                        brush_ = invis_mini
                    else:
                        brush_ = brush
                    nodes[i, j] = brush_ >> (x, y)

            # horizontal lines
            for j in [0, 2]:
                for i in range(len(xs)-1):
                    if i == 1:
                        connect_ldots(nodes[i, j], nodes[i+1, j])
                    else:
                        edge >> (nodes[i, j], nodes[i+1, j])

            # vertical lines
            for i in range(len(xs)):
                for j in range(len(ys)-1):
                    edge >> (nodes[i,j], nodes[i, j+1])


import fire
fire.Fire(Gradient)
