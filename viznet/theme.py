'''
defines themes for neural network and tensor networks.
'''

__all__ = ['NONE', 'YELLOW', 'GREEN', 'RED', 'BLUE', 'VIOLET', 'NODE_THEME_DICT']

# A TABLE OF PREDEFINED COLORS
NONE = 'none'
YELLOW = '#FFFF77'
GREEN = '#55CC77'
RED = '#FF6644'
BLUE = '#3399DD'
VIOLET = '#DD99DD'
BLACK = '#333333'

# COLOR | SHAPE | INSIDE_SHAPE | SHOW_EDGE
NODE_THEME_DICT = {
        'invisible': (None, 'none', 'circle', True),
        'basic': (NONE, 'none', 'circle', True),

        'nn.backfed': (YELLOW, 'circle', 'circle', True),
        'nn.input': (YELLOW, 'circle', 'none', True),
        'nn.noisy_input': (YELLOW, 'circle', 'triangle', True),
        'nn.hidden': (GREEN, 'circle', 'none', True),
        'nn.probablistic_hidden': (GREEN, 'circle', 'circle', True),
        'nn.spiking_hidden': (GREEN, 'circle', 'triangle', True),
        'nn.output': (RED, 'circle', 'none', True),
        'nn.match_input_output': (RED, 'circle', 'circle', True),
        'nn.recurrent': (BLUE, 'circle', 'none', True),
        'nn.memory': (BLUE, 'circle', 'circle', True),
        'nn.different_memory': (BLUE, 'circle', 'triangle', True),
        'nn.kernel': (VIOLET, 'circle', 'none', True),
        'nn.convolution': (VIOLET, 'circle', 'circle', True),
        'nn.pooling': (VIOLET, 'circle', 'circle', True),

        'tn.mps': (BLACK, 'circle', 'none', True),
        'tn.tri': (BLACK, 'triangle', 'none', True),
        'tn.tri_d': (BLACK, 'triangle_d', 'none', True),
        'tn.mpo': (BLACK, 'square', 'none', True)
}


EDGE_THEME_LIST = ['arrow', 'undirected', 'directed']
