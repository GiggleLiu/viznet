import numpy as np
import matplotlib.pyplot as plt
from viznet import DynamicShow, QuantumCircuit
from viznet import parsecircuit as _

def diffcircuit():
    '''illustration of block-focus scheme.'''
    num_bit = 4
    with DynamicShow((10, 4), '_differentiable.png') as ds:
        handler = QuantumCircuit(num_bit=num_bit)
        handler.x += 1.0
        with handler.block(slice(0, num_bit-1), pad_x=0.2, pad_y=0.1) as b:
            rot_gate(handler, 1, mask=[0,1,1])
        b[0].text('Rotation', 'top')
        handler.x += 1.0
        # entangler block
        with handler.block(slice(0, num_bit-1), pad_x=0, pad_y = 0.1) as b:
            entangle_gate(handler)
        b[0].text('Entangler', 'top')

        handler.x += 1.0
        rot_gate(handler, 2, mask=[1,1,1])
        handler.x += 1.0
        entangle_gate(handler)
        handler.x += 1.0
        rot_gate(handler, 3, mask=[1,1,0])

        handler.x += 1.0
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

def rot_gate(handler, l, mask=[True]*3):
    gates = ['Rz', 'Rx', 'Rz']
    for j, name in enumerate(gates):
        if not mask[j]: continue
        for i in range(handler.num_bit):
            handler.gate(_.WIDE, i, r'%s($\eta_%d^{%s}$)'%(name, l, chr(ord('a')+i*3+j)), fontsize=10)
        handler.x+=1.2
    if any(mask): handler.x-=1.2

def entangle_gate(handler):
    handler.gate((_.C, _.NOT), (1, 0))
    handler.gate((_.C, _.NOT), (3, 2))
    handler.x += 0.7
    handler.gate((_.C, _.NOT), (2, 0))
    handler.x += 0.7
    handler.gate((_.C, _.NOT), (3, 2))

if __name__ == '__main__':
    diffcircuit()
