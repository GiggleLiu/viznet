from ..netbasic import DynamicShow, NNPlot


def draw_prodnet(ax, num_node_visible):
    '''CNN to achieve MSR'''
    handler = NNPlot(ax)
    # visible layers
    handler.add_node_sequence(
        num_node_visible, '\sigma', offset=(0, 0), kind='input', radius=0.3, show_name=True)
    for i in [-1, num_node_visible]:
        handler.add_node('$\sigma_%d$' % (i + 1), (i - num_node_visible /
                                                   2. + 0.5, 0), kind='invisible', radius=0.3, show_name=False)
    for i in range(num_node_visible):
        A = '$nn_%d$' % (2 * i + 1)
        B = '$nn_%d$' % (2 * i + 2)
        with handler.context('fontsize', 10):
            handler.add_node(A, (i - num_node_visible / 2., 1),
                             kind='basic', radius=0.15, show_name=r'x')
            handler.add_node(B, (i - num_node_visible / 2. + 0.5, 1),
                             kind='basic', radius=0.15, show_name=r'x')
        handler.connect(A, r'$\sigma_%d$' % (i), directed=True)
        handler.connect(A, r'$\sigma_%d$' % (i + 1), directed=True)
        with handler.context('line_color', '#DD7733'):
            handler.connect(B, r'$\sigma_%d$' % (i), directed=True)
            handler.connect(B, r'$\sigma_%d$' % (i + 2), directed=True)
    # hidden layers
    handler.add_node_sequence(num_node_visible, 'h',
                              (-0.25, 2.0), kind='convolution', radius=0.3)

    # sum
    handler.add_node_sequence(1, r'+',
                              (-0.25, 3.0), kind='basic', radius=0.15, show_name=False)
    # psi
    handler.add_node_sequence(1, r'\psi',
                              (-0.25, 3.7), kind='output', radius=0.3, show_name=False)
    handler.text_node_sequence(r'+', text_list=[r'$+$'])
    handler.text_node_sequence(
        r'+', text_list=[r'$\sinh$'], offset=(-1.2, -0.2))
    handler.text_node_sequence(r'\psi', text_list=[r'$\psi$'])

    # connect them
    handler.connect_layers('nn', 'h', directed=True)
    handler.connect_layers('h', r'+', directed=False)
    handler.connect_layers('+', r'\psi', directed=True)


def test_prodnet():
    with DynamicShow((6, 4), '_prodnet.png') as d:
        draw_prodnet(d.ax, 6)


if __name__ == '__main__':
    test_prodnet()
