from ..netbasic import DynamicShow, NNPlot

def draw_conv_rbm(ax, num_node_visible, num_node_hidden):
    '''CNN equivalance to RBM'''
    handler = NNPlot(ax)
    # visible layers
    handler.add_node_sequence(
        num_node_visible, '\sigma^z', 0, kind='input', radius=0.3)

    # hidden layers
    handler.add_node_sequence(num_node_hidden, 'h',
                              1.5, kind='convolution', radius=0.3)

    # nonlinear layers
    handler.add_node_sequence(num_node_hidden, 'nonlinear',
                              2.3, kind='basic', radius=0.15, show_name=False)
    handler.text_node_sequence('nonlinear', text_list=[r'$\log 2\cosh$'], offset=(-0.55,-0.35))

    # sum
    handler.add_node_sequence(1, '+',
                              3.1, kind='basic', radius=0.15, show_name=False)
    handler.text_node_sequence('+', text_list=[r'$+$'])

    # output
    handler.add_node_sequence(1, r'\psi',
                              3.9, kind='output', radius=0.3, show_name=False)
    handler.text_node_sequence(r'\psi', text_list=[r'$\psi$'], offset=(0,0.))
    handler.text_node_sequence(r'\psi', text_list=[r'$\exp$'], offset=(-0.2,-0.5))

    # connect them
    handler.connect_layers('\sigma^z', 'h', directed=True)
    handler.connect_layers('h', 'nonlinear', directed=True, one2one=True)
    handler.connect_layers('nonlinear', '+', directed=False)
    handler.connect_layers('+', r'\psi', directed=True)

def test_conv_rbm():
    with DynamicShow((6, 6), '_conv_rbm.png') as d:
        draw_conv_rbm(d.ax, 5, 4)

if __name__ == '__main__':
    test_conv_rbm()
