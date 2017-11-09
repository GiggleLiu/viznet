from ..netbasic import DynamicShow, NNPlot
import matplotlib.pyplot as plt

def draw_caizi_nn(ax, num_node_visible, num_node_hidden):
    '''CaiZi R-Theta Network'''
    handler = NNPlot(ax)
    offset_amplitude = -num_node_hidden/2.
    offset_sign = num_node_hidden/2.-0.5
    # visible layers
    handler.add_node_sequence(
        num_node_visible, '\sigma^z', offset=(0,0), kind='input', radius=0.3)

    # hidden layers
    da, db = 0.8, 1.0
    y1 = db+0.5
    y2 = y1+da
    y3 = y2+db
    y4 = y3+da
    y5 = y4+da+0.3
    y6 = y5+da
    h1, h1p, h2 = 'h^{(1)}', 'h^{\prime(1)}', 'h^{(2)}'
    handler.add_node_sequence(num_node_hidden, h1,
                              kind='hidden', radius=0.3, offset=(offset_amplitude,y1))
    handler.add_node_sequence(1, h1p,
                              kind='hidden', radius=0.3, offset=(offset_sign, y1))

    # nonlinear layers
    handler.add_node_sequence(num_node_hidden, '\sigma1',
                              kind='basic', radius=0.2, show_name=False, offset=(offset_amplitude,y2))
    handler.add_node_sequence(1, '\cos',
                              kind='basic', radius=0.2, show_name=False, offset=(offset_sign,y2))
    handler.text_node_sequence(r'\sigma1', text_list=[r'$\sigma$'], offset=(-0.3,-0.3))

    # linear in amplitude
<<<<<<< HEAD
    handler.add_node_sequence(1, h2,
                              y3, kind='hidden', radius=0.3, show_name=True, offset=(offset_amplitude,0))
=======
    handler.add_node_sequence(1, 'linear2',
                              kind='hidden', radius=0.3, show_name=False, offset=(offset_amplitude,y3))
>>>>>>> eeffd14803ca7886c653b84f430ae0f73a4a8b73
    handler.add_node_sequence(1, '\sigma2',
                              kind='basic', radius=0.2, show_name=False, offset=(offset_amplitude,y4))

    # output
    sign_txt = r'\frac{\psi}{|\psi|}'
    handler.add_node_sequence(1, r'\times',
                              kind='basic', radius=0.2, show_name=False, offset=(-0.5,y5))
    handler.add_node_sequence(1, r'\psi',
                              kind='output', radius=0.3, show_name=False, offset=(-0.5,y6))
    handler.text_node_sequence(r'\psi', text_list=[r'$\psi$'], offset=(0.,0.))
    handler.text_node_sequence(r'\times', text_list=[r'$\times$'])
    handler.text_node_sequence(r'\cos', text_list=[r'$\cos$'], offset=(-0.3,-0.3))
    handler.text_node_sequence(r'\sigma2', text_list=[r'$\sigma$'], offset=(-0.3,-0.3))

    handler.fontsize = 10
    handler.text_node_sequence(r'\cos', text_list=[r'$%s$'%sign_txt])
    handler.text_node_sequence(r'\sigma2', text_list=[r'$|\psi|$'], offset=(0.,0.))

    # connect them
    handler.connect_layers('\sigma^z', h1, directed=True)
    handler.connect_layers('\sigma^z', h1p, directed=True)
    handler.connect_layers(h1, '\sigma1', directed=True, one2one=True)
    handler.connect_layers(h1p, '\cos', directed=True, one2one=True)
    handler.connect_layers('\sigma1', h2, directed=True)
    handler.connect_layers(h2, '\sigma2', directed=True)
    handler.connect_layers('\sigma2', r'\times', directed=False)
    handler.connect_layers('\cos', r'\times', directed=False)
    handler.connect_layers(r'\times', r'\psi', directed=True)

def draw_instance():
    with DynamicShow((5, 5), '_caizi.pdf') as d:
        draw_caizi_nn(d.ax, 5, 4)

if __name__ == '__main__':
    draw_instance()
