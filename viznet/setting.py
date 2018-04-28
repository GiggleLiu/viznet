'''
contains default settings for annotate, node, arrow and grid,
    * annotate_setting
    * node_setting
    * edge_setting

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
'''

node_setting = {
    'lw': 0.7,
    'edgecolor': 'k',
    'basesize': 1.0,

    'inner_lw': 0.7,
    'inner_edgecolor': 'k',
    'inner_facecolor': 'none',
}
'''
global node style setting
'''

edge_setting = {
    'arrow_head_width': 0.04,
    'arrow_head_length': 0.06,
    'doubleline_space': 0.016,
}
'''
global edge style setting
'''
