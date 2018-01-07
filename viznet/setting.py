'''
contains default settings for annotate, node, arrow and grid,
    * annotate_setting
    * node_setting
    * arrow_setting
    * grid_setting

Example:
    # disable edge for nodes

.. code-block:: python

    from viznet.setting import node_setting
    node_setting['lw'] = 0
'''

annotate_setting = {
    'fontsize': 12,
    'text_offset': 0.07,
}
'''
global text setting

.. code-block:: python

    annotate_setting = {
        'fontsize': 12,
        'text_offset': 0.07,
    }
'''
node_setting = {
    'lw': 0.7,
    'edgecolor': 'k',

    'inner_lw': 0.7,
    'inner_edgecolor': 'k',
    'inner_facecolor': 'none',
}
'''
global node style setting

.. code-block:: python

    node_setting = {
        'lw': 0.7,
        'edgecolor': 'k',

        'inner_lw': 0.7,
        'inner_edgecolor': 'k',
        'inner_facecolor': 'none',
    }
'''

arrow_setting = {
    'head_width': 0.04,
    'head_length': 0.06,
}
'''
global arrow style setting

.. code-block:: python

    arrow_setting = {
        'head_width': 0.04,
        'head_length': 0.06,
    }
'''

grid_setting = {
    'grid_width': 1,
    'grid_height': 1,
}
'''
plot grid (default space between two nodes) setting

.. code-block:: python

    grid_setting = {
        'grid_width': 1,
        'grid_height': 1,
    }
'''
