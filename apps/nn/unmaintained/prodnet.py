import matplotlib.pyplot as plt

from viznet import DynamicShow, NodeBrush, EdgeBrush, Layerwise

def draw_prodnet(ax, num_node_visible):
    '''CNN to achieve MSR'''
    handler = Layerwise()
    # brush
    conv = NodeBrush('nn.convolution', ax)
    input = NodeBrush('nn.input', ax)
    output = NodeBrush('nn.output', ax)
    invisible = NodeBrush('invisible', ax)
    op = NodeBrush('basic', ax, size='small')
    de = EdgeBrush('arrow', ax)
    ude = EdgeBrush('undirected', ax)
 
    # visible layers
    handler.node_sequence('\sigma', num_node_visible, offset=(0, 0), brush=input)
    handler.text('\sigma')
    for i in [-1, num_node_visible]:
        node = invisible >> (i - num_node_visible / 2. + 0.5, 0)
        ('$\sigma_%d$' % (i + 1), 
    for i in range(num_node_visible):
        A = '$nn_%d$' % (2 * i + 1)
        B = '$nn_%d$' % (2 * i + 2)
        with handler.context('fontsize', 10):
            handler.add_node(A, (i - num_node_visible / 2., 1),
                             kind='basic', radius=0.15, show_name=r'x')
            handler.add_node(B, (i - num_node_visible / 2. + 0.5, 1),
                             kind='basic', radius=0.15, show_name=r'x')
        handler.connecta2a(A, r'$\sigma_%d$' % (i), directed=True)
        handler.connecta2a(A, r'$\sigma_%d$' % (i + 1), directed=True)
        with handler.context('line_color', '#DD7733'):
            handler.connecta2a(B, r'$\sigma_%d$' % (i), directed=True)
            handler.connecta2a(B, r'$\sigma_%d$' % (i + 2), directed=True)
    # hidden layers
    handler.node_sequence('h', num_node_visible, 'h',
                              (-0.25, 2.0), kind='convolution', radius=0.3)

    # sum
    handler.node_sequence(r'+', 1,
                              (-0.25, 3.0), kind='basic', radius=0.15, show_name=False)
    # psi
    handler.node_sequence(r'\psi', 1,
                              (-0.25, 3.7), kind='output', radius=0.3, show_name=False)
    handler.text(r'+', text_list=[r'$+$'])
    handler.text(r'+', text_list=[r'$\sinh$'], offset=(-1.2, -0.2))
    plt.text(-1.45, 3.5, r'$\sinh$')
    handler.text(r'\psi', text_list=[r'$\psi$'])

    # connect them
    handler.connecta2a('nn', 'h', de)
    handler.connecta2a('h', r'+', ude)
    handler.connecta2a('+', r'\psi', de)


def test_prodnet():
    with DynamicShow((6, 4), '_prodnet.png') as d:
        draw_prodnet(d.ax, 6)


if __name__ == '__main__':
    test_prodnet()
