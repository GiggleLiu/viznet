import numpy as np
import viznet


def simple():
    '''(x1+x2)*x3'''
    num_node_visible = 6
    node = viznet.NodeBrush('nn.input', size='normal')
    op = viznet.NodeBrush('basic', size='small')
    edge = viznet.EdgeBrush('->-')
    with viznet.DynamicShow((4, 3), '_simple_cg.png') as d:
        # define brushes
        x1 = node >> (0, 0)
        x2 = node >> (0, 1)
        add = op >> (1, 0.5)
        edge >> (x1, add)
        edge >> (x2, add)

        x3 = node >> (1, 1.5)
        prod = op >> (2, 1.0)
        edge >> (x3, prod)
        edge >> (add, prod)
        prod.text(r'$\times$')
        add.text(r'$+$')
        x1.text('$x_1$')
        x2.text('$x_2$')
        x3.text('$x_3$')

def cgraph_layer(output='png'):
    '''computation graph for a typical single layer.'''
    with viznet.DynamicShow(figsize=(5,4), filename='_cg_layer.%s'%output) as ds:
        output = viznet.NodeBrush('nn.output', ds.ax)
        input = viznet.NodeBrush('nn.input', ds.ax)
        op = viznet.NodeBrush('basic', ds.ax)
        edge = viznet.EdgeBrush('->', ds.ax)
        x = input >> (0,0); x.text('$x$')
        dot = op >> (1,0); dot.text('dot'); dot.text('$f(W,x)=Wx$','top')
        W = input >> (1,-1); W.text('$W$')
        edge >> (x, dot)
        edge >> (W, dot)
        b = input >> (2,-1); b.text('$b$')
        plus = op >> (2,0); plus.text('$+$')
        edge >> (dot, plus)
        edge >> (b, plus)
        sigmoid = output >> (3,0); sigmoid.text(r'$\sigma$')
        edge >> (plus, sigmoid)

def cgraph_illu(output='png'):
    '''computation graph for simple mnist network.'''
    dx = 1
    dy = 1
    with viznet.DynamicShow(figsize=(3,2), filename='_cg_illu.%s'%output) as ds:
        op = viznet.NodeBrush('basic', ds.ax)
        edge = viznet.EdgeBrush('->', ds.ax)
        func1 = op >> (dx, 0); func1.text('$f$')
        inv1 = viznet.edgenode.Pin([0, 0])
        e1 = edge >> (inv1, func1)
        e1.text('input', 'top')
        func2 = op >> (0, -dy); func2.text('$f$')
        inv2 = viznet.edgenode.Pin([dx, -dy])
        e2 = edge >> (func2, inv2)
        e2.text('output', 'top')

def cgraph_mnist_full(output='png'):
    '''computation graph for simple mnist network.'''
    with viznet.DynamicShow(figsize=(3,6), filename='_cg_mnist_full.%s'%output) as ds:
        output = viznet.NodeBrush('nn.output', ds.ax)
        input = viznet.NodeBrush('nn.input', ds.ax)
        op = viznet.NodeBrush('basic', ds.ax)
        edge = viznet.EdgeBrush('->', ds.ax)
        x = input >> (0, 0); x.text('$x$')
        dot = op >> (0, -1); dot.text('dot')
        W = input >> (-1, -1); W.text('$W$')
        edge >> (x, dot)
        edge >> (W, dot)
        b = input >> (-1, -2); b.text('$b$')
        plus = op >> (0, -2); plus.text('$+$')
        edge >> (dot, plus)
        edge >> (b, plus)
        softmax = op >> (0, -3); softmax.text(r'Softmax', 'left')
        edge >> (plus, softmax)
        crossentropy = op >> (0, -4); crossentropy.text(r'CrossEntropy', 'left')
        y = input >> (1, -4); y.text(r'$y$')
        edge >> (softmax, crossentropy)
        edge >> (y, crossentropy)
        mean = output >> (0, -5); mean.text(r'Mean')
        edge >> (crossentropy, mean)

if __name__ == '__main__':
    #simple()
    #cgraph_illu()
    cgraph_mnist_full()
    #cgraph_layer()
