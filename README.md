# Viznet - A Neural Network visualization toolbox

## To Run a Sample
```bash
    $ python -m viznet.tests.test_netbasic
```

I created a theme for neural network plotting following [Neural Network Zoo Page](http://www.asimovinstitute.org/neural-network-zoo/),
here is a table of node species:

For Neural Network, we have

![theme_list](docs/images/nn_theme_list.png)

For Tensor Network, we have

![theme_list](docs/images/tn_theme_list.png)

Besides, we have two basic types, basic and invisible.

![theme_list](docs/images/theme_list.png)




```python
# COLOR | SHAPE | INSIDE_SHAPE
NODE_THEME_DICT = {
        'invisible': (None, 'circle', 'none'),
        'basic': (NONE, 'circle', 'none'),

        'nn.backfed': (YELLOW, 'circle', 'circle'),
        'nn.input': (YELLOW, 'circle', 'none'),
        'nn.noisy_input': (YELLOW, 'circle', 'triangle'),
        'nn.hidden': (GREEN, 'circle', 'none'),
        'nn.probablistic_hidden': (GREEN, 'circle', 'circle'),
        'nn.spiking_hidden': (GREEN, 'circle', 'triangle'),
        'nn.output': (RED, 'circle', 'none'),
        'nn.match_input_output': (RED, 'circle', 'circle'),
        'nn.recurrent': (BLUE, 'circle', 'none'),
        'nn.memory': (BLUE, 'circle', 'circle'),
        'nn.different_memory': (BLUE, 'circle', 'triangle'),
        'nn.kernel': (VIOLET, 'circle', 'none'),
        'nn.convolution': (VIOLET, 'circle', 'circle'),
        'nn.pooling': (VIOLET, 'circle', 'circle'),

        'tn.mps': (BLACK, 'circle', 'none'),
        'tn.tri': (BLACK, 'triangle', 'none'),
        'tn.tri_u': (BLACK, 'triangle-u', 'none'),
        'tn.tri_d': (BLACK, 'triangle-d', 'none'),
        'tn.tri_l': (BLACK, 'triangle-l', 'none'),
        'tn.tri_r': (BLACK, 'triangle-r', 'none'),
        'tn.mpo': (BLACK, 'square', 'none'),
        'tn.mpo21': (BLACK, 'rectangle-2-1', 'none'),
        'tn.mpo12': (BLACK, 'rectangle-1-2', 'none'),
}
```

## Example A: Time Evolving Block Decimation

![theme_list](docs/images/tebd.png)

```python
from viznet import theme, NodeBrush, EdgeBrush, DynamicShow

def tebd():
    with DynamicShow((6, 4), filename='tebd.png') as ds:
        # define a set of brushes.
        # NodeBrush can place a node at some location, like `node_brush >> (x, y)`,
        # and it will return a Node instance.
        # EdgeBrush can connect two Nodes (or Pin as a special Node),
        # like `edge_brush >> node_a, node_b`, and will return an Edge instance.
        size = 'normal'
        mps = NodeBrush('tn.mps', ds.ax, size=size)
        # invisible node can be used as a placeholder
        invisible_mps = NodeBrush('invisible', ds.ax, size=size)
        mpo21 = NodeBrush('tn.mpo21', ds.ax, size=size)
        edge = EdgeBrush('undirected', ds.ax, lw=2.)

        # add a sequence of mps nodes, a store them in a list for future use.
        mps_list = []
        for i in range(8):
            mps_list.append(mps >> (i, 0))
            mps_list[-1].text(r'$\sigma_%d$' % i, position='bottom')
        mps_list.append(invisible_mps >> (i + 1, 0))

        # add mpo and connect nodes
        for layer in range(4):
            # set brush color, it will overide theme color!
            # You can set brush color to None to restore theme color.
            mpo21.color = theme.RED if layer % 2 == 0 else theme.GREEN
            mpo_list = []
            start = layer % 2
            for i, (mps_l, mps_r) in enumerate(zip(mps_list[start::2],
                                                   mps_list[start + 1::2])):
                # place an two site mpo slightly above the center of two mps nodes
                mpo_list.append(mpo21 >> (mps_l.position +
                                          mps_r.position) / 2. + (0, layer + 1))
                if layer == 0:
                    # if this is the first mpo layer, connect mps and newly added mpo.
                    pin_l = mps_l
                    pin_r = mps_r
                else:
                    # otherwise, place a pin at the top surface of previous mpo,
                    # we also require it horizontally aligned to some `mps_l` object.
                    # pin is a special node, which is zero sized,
                    # we can use it to connect nodes, add texts.
                    # if you're about to place some pin at `left` or
                    # `right` surface of a node,
                    # align is then intepreted as vertial align.
                    pin_l = mpo_list_pre[i].pin('top', align=mps_l)
                    pin_r = mpo_list_pre[i].pin('top', align=mps_r)
                if layer < 2:
                    edge >> (mps_l, mps_r)
                edge >> (pin_l, mpo_list[-1].pin('bottom', align=mps_l))
                edge >> (pin_r, mpo_list[-1].pin('bottom', align=mps_r))
            mpo_list_pre = mpo_list


if __name__ == '__main__':
    tebd()
```

## Example B: Restricted Boltzmann Machine

![theme_list](docs/images/rbm.png)
To get this graph, you can run the following code
```python
import numpy as np
from viznet import NodeBrush, DynamicShow, Layerwise, EdgeBrush


def test_draw_bm():
    '''Draw a Boltzmann Machine'''
    num_node_visible = 6
    with DynamicShow((5, 4), '_bm.pdf') as d:
        # define brushes
        node = NodeBrush('nn.backfed', d.ax, size='normal')
        edge = EdgeBrush('undirected', d.ax)

        node_list = add_circled_node_sequence(
            num_node_visible, node, radius=1.0, offset=(0, 0))

        # connect all
        for i, nodei in enumerate(node_list):
            # add text
            nodei.text(r'$\sigma_%d$' % i)
            for nodej in node_list:
                if nodei is not nodej:
                    edge >> (nodei, nodej)


def add_circled_node_sequence(num_node, brush, radius, offset=(0, 0)):
    '''
    add a sequence of nodes placed on a ring.

    Args:
        num_node (int): number of node to be added.
        brush (:obj:`NodeBrush`): node brush.
        radius (float): the raidus of the ring.
        offset (tuple|float): offset in x-y directions.

    Return:
        list: a list of nodes
    '''
    theta_list = np.arange(0, 2 * np.pi, 2 * np.pi / num_node)
    R = radius * num_node / np.pi
    xylist = np.array([np.cos(theta_list), np.sin(theta_list)]).T * R

    node_list = []
    i = 0
    for xy in xylist:
        node_list.append(brush >> xy)
        i += 1
    return node_list


if __name__ == '__main__':
    test_draw_bm()
```

## Example C: Convolutional Neural Network on quivalence of RBM
![theme_list](docs/images/conv_rbm.png)

In this example, I will use `viznet.Layerwise` utility to manipulate (connect/text) nodes in a layer,
the code looks like

```python
from viznet import *

def draw_conv_rbm(ax, num_node_visible, num_node_hidden):
    '''CNN equivalance to RBM'''
    handler = Layerwise()
    # brush
    conv = NodeBrush('nn.convolution', ax)
    input = NodeBrush('nn.input', ax)
    output = NodeBrush('nn.output', ax)
    op = NodeBrush('basic', ax, size='small')
    de = EdgeBrush('arrow', ax)
    ude = EdgeBrush('undirected', ax)

    # visible layers
    handler.node_sequence('\sigma^z', num_node_visible, offset=(0, 0), brush=input)

    # hidden layers
    handler.node_sequence('h', num_node_hidden, offset=(0, 1.5), brush=conv)

    # nonlinear layers
    handler.node_sequence('nonlinear', num_node_hidden, offset=(0, 2.3), brush = op)

    # sum
    handler.node_sequence('+', 1, offset=(0, 3.1), brush = op)

    # output
    psi = handler.node_sequence(r'\psi', 1, offset=(0, 3.9), brush=output)

    # text nodes
    handler.text('\sigma^z')
    handler.text('h')
    handler.text(r'\psi', text_list=[r'$\psi$'])
    handler.text(r'\psi', text_list=[r'$\exp$'], position='left')
    handler.text('+', text_list=[r'$+$'])
    handler.text('nonlinear', [r'$\log 2\cosh$'], position='left')

    # connect them
    # all to all connection
    handler.connecta2a('\sigma^z', 'h', de)
    # one to one connection
    handler.connect121('h', 'nonlinear', de)
    handler.connecta2a('nonlinear', '+', ude)
    handler.connect121('+', '\psi', de)


def test_conv_rbm():
    with DynamicShow((6, 6), '_conv_rbm.png') as d:
        draw_conv_rbm(d.ax, 5, 4)


if __name__ == '__main__':
    test_conv_rbm()
```
