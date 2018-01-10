from viznet import *


def draw_conv_rbm(ax, num_node_visible, num_node_hidden):
    '''CNN equivalance to RBM'''
    handler = Layerwise()
    # brush
    conv = NodeBrush('nn.convolution', ax)
    input = NodeBrush('nn.input', ax)
    output = NodeBrush('nn.output', ax)
    op = NodeBrush('basic', ax, size='small')
    de = EdgeBrush('-->', ax)
    ude = EdgeBrush('---', ax)

    # visible layers
    handler.node_sequence(r'\sigma^z', num_node_visible,
                          offset=(0, 0), brush=input)

    # hidden layers
    handler.node_sequence('h', num_node_hidden, offset=(0, 1.5), brush=conv)

    # nonlinear layers
    handler.node_sequence('nonlinear', num_node_hidden,
                          offset=(0, 2.3), brush=op)

    # sum
    handler.node_sequence('+', 1, offset=(0, 3.1), brush=op)

    # output
    psi = handler.node_sequence(r'\psi', 1, offset=(0, 3.9), brush=output)

    # text nodes
    handler.text(r'\sigma^z')
    handler.text('h')
    handler.text(r'\psi', text_list=[r'$\psi$'])
    handler.text(r'\psi', text_list=[r'$\exp$'], position='left')
    handler.text('+', text_list=[r'$+$'])
    handler.text('nonlinear', [r'$\log 2\cosh$'], position='left')

    # connect them
    handler.connecta2a(r'\sigma^z', 'h', de)
    handler.connect121('h', 'nonlinear', de)
    handler.connecta2a('nonlinear', '+', ude)
    handler.connect121('+', r'\psi', de)


def test_conv_rbm():
    with DynamicShow((6, 6), '_conv_rbm.png') as d:
        draw_conv_rbm(d.ax, 5, 4)


if __name__ == '__main__':
    test_conv_rbm()
