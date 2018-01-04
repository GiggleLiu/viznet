from viznet import *
import matplotlib.pyplot as plt


def draw_caizi_nn(ax, num_node_visible, num_node_hidden):
    '''CaiZi R-Theta Network'''
    handler = Layerwise()
    # brush
    conv = NodeBrush('nn.convolution', ax)
    input = NodeBrush('nn.input', ax)
    hidden = NodeBrush('nn.hidden', ax)
    output = NodeBrush('nn.output', ax)
    op = NodeBrush('basic', ax, size='small')
    de = EdgeBrush('arrow', ax)
    ude = EdgeBrush('undirected', ax)

    # parameters
    offset_amplitude = -num_node_hidden / 2.
    offset_sign = num_node_hidden / 2. - 0.5
    # visible layers
    handler.node_sequence('\sigma^z', num_node_visible, input, offset=(0, 0))

    # hidden layers
    da, db = 0.8, 1.0
    y1 = db + 0.5
    y2 = y1 + da
    y3 = y2 + db
    y4 = y3 + da
    y5 = y4 + da + 0.3
    y6 = y5 + da
    h1, h1p, h2 = 'h^{(1)}', 'h^{\prime(1)}', 'h^{(2)}'
    handler.node_sequence(h1, num_node_hidden, hidden,
                          offset=(offset_amplitude, y1))
    handler.node_sequence(h1p, 1, hidden, offset=(offset_sign, y1))

    # nonlinear layers
    handler.node_sequence('\sigma1', num_node_hidden, op,
                          offset=(offset_amplitude, y2))
    handler.node_sequence('\cos', 1, op,
                          offset=(offset_sign, y2))
    handler.text(r'\sigma1', text_list=[r'$\sigma$'], position='left')

    # linear in amplitude
    handler.node_sequence(h2, 1, hidden, offset=(offset_amplitude, y3))
    handler.node_sequence('\sigma2', 1, op,
                          offset=(offset_amplitude, y4))

    # output
    sign_txt = r'\frac{\psi}{|\psi|}'
    handler.node_sequence(r'\times', 1, op, offset=(-0.5, y5))
    handler.node_sequence(r'\psi', 1, output, offset=(-0.5, y6))
    handler.text(h1)
    handler.text(h1p)
    handler.text(h2)
    handler.text(r'\psi', text_list=[r'$\psi$'])
    handler.text(r'\times', text_list=[r'$\times$'])
    handler.text(
        r'\cos', text_list=[r'$\cos$'], position='left')
    handler.text(r'\sigma2', text_list=[
        r'$\sigma$'], position='left')

    handler.fontsize = 10
    handler.text(r'\cos', text_list=[r'$%s$' % sign_txt])
    handler.text(r'\sigma2', text_list=[r'$|\psi|$'])

    # connect them
    handler.connecta2a('\sigma^z', h1, de)
    handler.connecta2a('\sigma^z', h1p, de)
    handler.connect121(h1, '\sigma1', de)
    handler.connect121(h1p, '\cos', de)
    handler.connecta2a('\sigma1', h2, de)
    handler.connecta2a(h2, '\sigma2', de)
    handler.connecta2a('\sigma2', r'\times', ude)
    handler.connecta2a('\cos', r'\times', ude)
    handler.connecta2a(r'\times', r'\psi', de)


def draw_instance():
    with DynamicShow((5, 5), '_caizi.pdf') as d:
        draw_caizi_nn(d.ax, 5, 4)


if __name__ == '__main__':
    draw_instance()
