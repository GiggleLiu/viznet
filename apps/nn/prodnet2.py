import matplotlib.pyplot as plt
from viznet import DynamicShow, Layerwise, NodeBrush, EdgeBrush


def draw_prodnet2(ax, num_node_visible):
    '''CNN to achieve MSR'''
    handler = Layerwise()
    # brush
    conv = NodeBrush('nn.convolution', ax)
    input = NodeBrush('nn.input', ax)
    output = NodeBrush('nn.output', ax)
    op = NodeBrush('basic', ax, size='small')
    de = EdgeBrush('arrow', ax)
    ude = EdgeBrush('undirected', ax)

    da = 0.6
    db = 0.8
    y = 0
    # visible layers
    handler.node_sequence('\sigma', num_node_visible, input, offset=(0, y))
    y += da
    # log
    handler.node_sequence('\log', num_node_visible, op, offset=(0, y))
    y += db
    # hidden layers
    handler.node_sequence('h', num_node_visible, conv, (0, y))
    y += da

    # exp
    handler.node_sequence('\exp', num_node_visible, op, offset=(0, y))

    # psi
    plt.text(0, 2.7, r'$\ldots$', va='center', ha='center', fontsize=22)
    handler.node_sequence(r'\psi', 1, output, (0, 3.5))

    # annotate nodes
    handler.text('\sigma')
    handler.text('h')
    handler.text(r'\psi', text_list=[r'$\psi$'])
    handler.text(r'\log', text_list=[r'$\log$'], position='left')
    handler.text(r'\exp', text_list=[r'$\exp$'], position='left')

    # connect them
    handler.connect121('\sigma', '\log', de)
    handler.connecta2a('\log', 'h', de)
    handler.connect121('h', '\exp', de)


def test_prodnet2():
    with DynamicShow((6, 4), '_prodnet2.png') as d:
        draw_prodnet2(d.ax, 6)


if __name__ == '__main__':
    test_prodnet2()
