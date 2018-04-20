import pdb
import numpy as np
import matplotlib.pyplot as plt
from viznet import NodeBrush, DynamicShow, QuantumCircuit, Pin

def focus(handler, lines):
    '''focus to target lines.'''
    alllines = range(handler.num_bit)
    pin = NodeBrush('pin')
    old_positions = []
    for i in range(handler.num_bit):
        old_positions.append(handler.gate(pin, i))

    lmap = np.append(lines, np.setdiff1d(alllines, lines))
    handler.x += 0.8
    for opos, j in zip(old_positions, lmap):
        pi = Pin(handler.get_position(j))
        handler.node_dict[j].append(pi)
        handler.edge >> (opos, pi)

def ghz4():
    '''4 bit GHZ circuit, applicable on ibmqx4 circuit.'''
    num_bit = 6
    with DynamicShow((5, 3), '_blockfocus.pdf') as ds:
        basic = NodeBrush('qc.basic')
        C = NodeBrush('qc.C')
        NOT = NodeBrush('qc.NOT', size='small')
        END = NodeBrush('qc.end')
        M = NodeBrush('qc.measure')
        block = NodeBrush('art.rbox', size=(2, 2), ls='--')

        handler = QuantumCircuit(num_bit=num_bit)
        handler.x += 0.8
        handler.gate(basic, 0, 'X')
        for i in range(1, num_bit):
            handler.gate(basic, i, 'H')
        handler.x += 0.8
        handler.focus([4, 2, 1, 3])
        handler.x += 0.8

        # entangler block
        with handler.block(block, 0, 3) as b:
            handler.gate((C, NOT), (1, 0))
            handler.gate((C, NOT), (3, 2))
            handler.x += 0.7
            handler.gate((C, NOT), (2, 0))
            handler.x += 0.7
            handler.gate((C, NOT), (3, 2))
        b[0].text('entangler', 'top')

        handler.x += 1
        for i in range(num_bit):
            handler.gate(basic, i, 'H')
        handler.x += 1
        for i in range(num_bit):
            handler.gate(M, i)
        handler.edge.style = '='
        handler.x += 0.8
        for i in range(num_bit):
            handler.gate(END, i)

        # text |0>s
        for i in range(num_bit):
            plt.text(-0.5, -i, r'$\left\vert0\right\rangle_{Q_%d}$' %
                     i, va='center', ha='center', fontsize=18)


if __name__ == '__main__':
    ghz4()
