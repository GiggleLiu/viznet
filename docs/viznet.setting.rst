.. _viznet.setting:

viznet.setting
==================

.. toctree::
	:maxdepth: 2

Module contents
---------------

.. automodule:: viznet.setting

.. exec::
    import json
    from viznet import setting
    for var in ['annotate', 'node', 'edge']:
        print('.. autodata:: viznet.setting.%s_setting\n'%var)
        json_obj = json.dumps(eval('setting.%s_setting'%var), sort_keys=True, indent=4)
        print('.. code-block:: JavaScript\n\n    %s_setting = %s    }\n\n' % (var, json_obj[:-1]))
