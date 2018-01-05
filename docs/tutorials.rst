.. _tutorial:

Tutorial
========

.. toctree::
   :maxdepth: 2	

Getting started
---------------

To start using Layers, simply

`clone/download <https://159.226.35.226/jgliu/PoorNN.git>`_ this repo and run

.. code-block:: bash

    $ cd PoorNN/
    $ pip install -r requirements.txt
    $ python setup.py install

Node and Edge Brush
---------------------------
To define a node, 

.. code-block:: python

    brush = NodeBrush('nn.input')
    node1 = brush >> (1,0)
    node2 = brush >> (2,0)
    edge >> (node1, node2)


Pins
---------------------------

Layerwise operation
---------------------------
.. note::

    This is a note.


