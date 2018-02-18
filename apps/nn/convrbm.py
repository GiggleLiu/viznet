from viznet import *


def draw_conv_rbm(ax, num_node_visible, num_node_hidden):
    '''CNN equivalance to RBM'''
    # brush
    conv = NodeBrush('nn.convolution', ax)
    input = NodeBrush('nn.input', ax)
    output = NodeBrush('nn.output', ax)
    op = NodeBrush('basic', ax, size='small')
    de = EdgeBrush('-->', ax)
    ude = EdgeBrush('---', ax)

    # visible layers
    sigma = node_sequence(input, num_node_visible, center=(0, 0))

    # hidden layers
    h = node_sequence(conv, num_node_hidden, center=(0, 1.5))

    # nonlinear layers
    nonlinear = node_sequence(op, num_node_hidden, center=(0, 2.3))

    # sum
    sum_op = op >> (0, 3.1)

    # output
    psi = output >> (0, 3.9)

    # text nodes
    for node_list, base_string in zip([sigma, h], ['\sigma^z', 'h']):
        for i, node in enumerate(node_list):
            node.text('$%s_%d$'%(base_string, i))
    nonlinear[0].text(r'$\log 2\cosh$', position='left')
    psi.text(r'$\psi$')
    psi.text(r'$\exp$', position='left')
    sum_op.text(r'$+$')

    # connect them
    connecta2a(sigma, h, de)
    connect121(h, nonlinear, de)
    connecta2a(nonlinear, [sum_op], ude)
    de >> (sum_op, psi)


def test_conv_rbm():
    with DynamicShow((6, 6), '_conv_rbm.png') as d:
        draw_conv_rbm(d.ax, 5, 4)


if __name__ == '__main__':
    test_conv_rbm()
