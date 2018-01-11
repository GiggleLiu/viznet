.. _viznet.theme:

viznet.theme
==============

.. toctree::
	:maxdepth: 2

Module contents
---------------

.. autodata:: viznet.theme.NODE_THEME_DICT
    :annotation:

.. exec::
    import json
    from viznet.theme import NODE_THEME_DICT
    json_obj = json.dumps(NODE_THEME_DICT, sort_keys=True, indent=4)
    print('.. code-block:: JavaScript\n\n    NODE_THEME_DICT = %s    }\n\n' % json_obj[:-1])
