from viznet import *
import matplotlib.pyplot as plt


def draw_caizi_nn(ax, num_node_visible, num_node_hidden):
    '''CaiZi R-Theta Network'''
    # brush
    conv = NodeBrush('nn.convolution', ax)
    input = NodeBrush('nn.input', ax)
    hidden = NodeBrush('nn.hidden', ax)
    output = NodeBrush('nn.output', ax)
    op = NodeBrush('basic', ax, size='small')
    de = EdgeBrush('-->', ax)
    ude = EdgeBrush('---', ax)

    # parameters
    offset_amplitude = -num_node_hidden / 2.
    offset_sign = num_node_hidden / 2. - 0.5
    # visible layers
    sigma = node_sequence(input, num_node_visible, center=(0, 0))

    # hidden layers
    da, db = 0.8, 1.0
    y1 = db + 0.5
    y2 = y1 + da
    y3 = y2 + db
    y4 = y3 + da
    y5 = y4 + da + 0.3
    y6 = y5 + da
    h1_text, h1p_text, h2_text = 'h^{(1)}', '$h^{\prime(1)}$', '$h^{(2)}$'
    h1 = node_sequence(hidden, num_node_hidden,
                          center=(offset_amplitude, y1))
    h1p = hidden >> (offset_sign, y1)

    # nonlinear layers
    sigma1 = node_sequence(op, num_node_hidden,
                          center=(offset_amplitude, y2))
    cos = op >> (offset_sign, y2)

    # linear in amplitude
    h2 = hidden >> (offset_amplitude, y3)
    sigma2 = op >> (offset_amplitude, y4)

    # output
    sign_txt = r'\frac{\psi}{|\psi|}'
    times = op >> (-0.5, y5)
    psi = output >> (-0.5, y6)
    for node_list, base_string in zip([sigma, h1], ['\sigma^z', h1_text]):
        for i, node in enumerate(node_list):
            node.text('$%s_%d$'%(base_string, i))
    h1p.text(h1p_text)
    h2.text(h2_text)
    psi.text(r'$\psi$')
    times.text(r'$\times$')
    cos.text(r'$\cos$', position='left')
    sigma1[0].text(r'$\sigma$', position='left')

    cos.text(r'$%s$' % sign_txt, fontsize=10)
    sigma2.text(r'$|\psi|$')

    # connect them
    connecta2a(sigma, h1, de)
    connecta2a(sigma, [h1p], de)
    connect121(h1, sigma1, de)
    connecta2a(sigma1, [h2], de)
    de >> (h1p, cos)
    de >> (h2, sigma2)
    ude >> (sigma2, times)
    ude >> (cos, times)
    de >> (times, psi)


def draw_instance():
    with DynamicShow((5, 5), '_caizi.pdf') as d:
        draw_caizi_nn(d.ax, 5, 4)


if __name__ == '__main__':
    draw_instance()
