from ..netbasic import DynamicShow, NNPlot


def draw_conv_msr(ax, num_node_visible):
    '''CNN to achieve MSR'''
    handler = NNPlot(ax)
    # visible layers
    with handler.context('distance', (2, 0)) as b:
        handler.add_node_sequence(
            num_node_visible / 2, 'even', offset=(-0.5, 0), kind='input', radius=0.3, show_name=False)
        handler.add_node_sequence(
            num_node_visible / 2, 'odd', offset=(0.5, 0), kind='input', radius=0.3, show_name=False)
        # hidden layers
        handler.add_node_sequence(num_node_visible / 2, 'h',
                                  0.6, kind='convolution', radius=0.3)

    # sum
    handler.add_node_sequence(1, r'+',
                              2.8, kind='basic', radius=0.15, show_name=False)
    handler.add_node_sequence(1, r'\theta',
                              3.6, kind='basic', radius=0., show_name=False)
    handler.text_node_sequence(r'+', text_list=[r'$+$'])
    handler.text_node_sequence(r'\theta', text_list=[
                               r'$\theta$'], offset=(-0.2, 0))
    handler.text_node_sequence(
        r'even', text_list=[r'$\sigma_%d$' % i for i in range(1, num_node_visible, 2)])
    handler.text_node_sequence(r'odd', text_list=[
                               r'$\sigma_%d$' % i for i in range(2, num_node_visible + 1, 2)])

    # connect them
    with handler.context('line_color', '#AA3333'):
        handler.connect_layers('odd', 'h', directed=True, one2one=True)
    handler.connect_layers('even', 'h', directed=True, one2one=True)
    handler.connect_layers('h', r'+', directed=False)
    handler.connect_layers('+', r'\theta', directed=True)


def test_conv_msr():
    with DynamicShow((6, 6), '_conv_msr.png') as d:
        draw_conv_msr(d.ax, 8)


if __name__ == '__main__':
    test_conv_msr()
