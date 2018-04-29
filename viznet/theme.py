'''
defines themes for neural network and tensor networks.
'''

__all__ = ['NONE', 'YELLOW', 'GREEN', 'RED',
           'BLUE', 'VIOLET', 'NODE_THEME_DICT']

# A TABLE OF PREDEFINED COLORS
NONE = 'none'
YELLOW = '#FFFF77'
GREEN = '#55CC77'
RED = '#FF6644'
BLUE = '#3399DD'
VIOLET = '#DD99DD'
BLACK = '#333333'

# COLOR | SHAPE | INSIDE_SHAPE
NODE_THEME_DICT = {
    'invisible': (None, 'circle', 'none'),
    'basic': (NONE, 'circle', 'none'),
    'box': (NONE, 'rectangle', 'none'),
    'pin': (None, 'empty', 'none'),

    'nn.backfed': (YELLOW, 'circle', 'circle'),
    'nn.input': (YELLOW, 'circle', 'none'),
    'nn.noisy_input': (YELLOW, 'circle', 'triangle'),
    'nn.hidden': (GREEN, 'circle', 'none'),
    'nn.probablistic_hidden': (GREEN, 'circle', 'circle'),
    'nn.spiking_hidden': (GREEN, 'circle', 'triangle'),
    'nn.output': (RED, 'circle', 'none'),
    'nn.match_input_output': (RED, 'circle', 'circle'),
    'nn.recurrent': (BLUE, 'circle', 'none'),
    'nn.memory': (BLUE, 'circle', 'circle'),
    'nn.different_memory': (BLUE, 'circle', 'triangle'),
    'nn.kernel': (VIOLET, 'circle', 'none'),
    'nn.convolution': (VIOLET, 'circle', 'circle'),
    'nn.pooling': (VIOLET, 'circle', 'circle'),

    'tn.mps': (BLACK, 'circle', 'none'),
    'tn.tri': (BLACK, 'triangle', 'none'),
    'tn.mpo': (BLACK, 'rectangle', 'none'),
    'tn.dia': (BLACK, 'diamond', 'none'),

    'qc.basic': (NONE, 'square', 'none'),
    'qc.wide': (NONE, 'golden', 'none'),
    'qc.C': (None, 'empty', 'dot'),
    'qc.NC': ('none', 'circle', 'none'),
    'qc.cross': (None, 'empty', 'cross'),
    'qc.NOT': (NONE, 'circle', 'plus'),
    'qc.measure': (NONE, 'golden', 'measure'),
    'qc.end': (None, 'empty', 'vbar'),
    'qc.box': (NONE, 'rectangle', 'none'),
}
'''
A table of theme for nodes.
values are `COLOR | SHAPE | INNER_SHAPE`.
'''
