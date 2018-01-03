import matplotlib.pyplot as plt
from ..netbasic import DynamicShow, NNPlot


def draw_prodnet2(ax, num_node_visible):
    '''CNN to achieve MSR'''
    handler = NNPlot(ax)
    da = 0.6
    db = 0.8
    y = 0
    # visible layers
    handler.add_node_sequence(
        num_node_visible, '\sigma', offset=(0, y), kind='input', radius=0.3, show_name=True)
    y += da
    # log
    handler.add_node_sequence(
        num_node_visible, '\log', offset=(0, y), kind='basic', radius=0.15, show_name=False)
    y += db
    # hidden layers
    handler.add_node_sequence(num_node_visible, 'h',
                              (0, y), kind='convolution', radius=0.3)
    y += da

    # exp
    handler.add_node_sequence(
        num_node_visible, '\exp', offset=(0, y), kind='basic', radius=0.15, show_name=False)

    # psi
    plt.text(0, 2.7, r'$\ldots$', va='center', ha='center', fontsize=22)
    handler.add_node_sequence(1, r'\psi',
                              (0, 3.5), kind='output', radius=0.3, show_name=False)
    handler.text_node_sequence(r'\psi', text_list=[r'$\psi$'])
    handler.text_node_sequence(
        r'\log', text_list=[r'$\log$'], offset=(-0.3, -0.2))
    handler.text_node_sequence(
        r'\exp', text_list=[r'$\exp$'], offset=(-0.3, -0.2))
    handler.text_node_sequence(r'\psi', text_list=[r'$\psi$'])

    # connect them
    handler.connect_layers('\sigma', '\log', directed=True, one2one=True)
    handler.connect_layers('\log', 'h', directed=True)
    handler.connect_layers('h', '\exp', directed=True, one2one=True)


def test_prodnet2():
    with DynamicShow((6, 4), '_prodnet2.png') as d:
        draw_prodnet2(d.ax, 6)


if __name__ == '__main__':
    test_prodnet2()
