import numpy as np
import matplotlib.pyplot as plt
from viznet import DynamicShow, QuantumCircuit
from viznet import parsecircuit as _

def blockfocus():
    '''illustration of block-focus scheme.'''
    num_bit = 6
    with DynamicShow((5, 3), '_blockfocus.png') as ds:
        handler = QuantumCircuit(num_bit=num_bit)
        handler.x += 0.8
        handler.gate(_.GATE, 0, 'X')
        for i in range(1, num_bit):
            handler.gate(_.GATE, i, 'H')
        handler.x += 1.2
        with handler.block(slice(0, num_bit-1), pad_x=0.1) as b:
            handler.focus([4, 2, 1, 3])
        b[0].text('focus', 'top')
        handler.x += 1.2

        # entangler block
        with handler.block(slice(0, 3)) as b:
            handler.gate((_.C, _.NOT), (1, 0))
            handler.gate((_.C, _.NOT), (3, 2))
            handler.x += 0.7
            handler.gate((_.C, _.NOT), (2, 0))
            handler.x += 0.7
            handler.gate((_.C, _.NOT), (3, 2))
        b[0].text('entangler', 'top')

        handler.x += 1.2
        for i in range(num_bit):
            handler.gate(_.GATE, i, 'H')
        handler.x += 1
        for i in range(num_bit):
            handler.gate(_.MEASURE, i)
        handler.edge.style = '='
        handler.x += 0.8
        for i in range(num_bit):
            handler.gate(_.END, i)

        # text |0>s
        for i in range(num_bit):
            plt.text(-0.5, -i, r'$\left\vert0\right\rangle$'
                     , va='center', ha='center', fontsize=16)


if __name__ == '__main__':
    blockfocus()
