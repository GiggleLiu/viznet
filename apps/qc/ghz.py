import matplotlib.pyplot as plt
from viznet import DynamicShow, QuantumCircuit
from viznet import parsecircuit as _


def ghz4():
    '''4 bit GHZ circuit, applicable on ibmqx4 circuit.'''
    num_bit = 4
    with DynamicShow((5, 3), '_exact_ghz4_circuit.png') as ds:
        handler = QuantumCircuit(num_bit=4, y0=2.)
        handler.x += 0.5
        handler.gate(_.GATE, 0, 'X')
        for i in range(1, num_bit):
            handler.gate(_.GATE, i, 'H')
        handler.x += 1
        handler.gate((_.C, _.NOT), (1, 0))
        handler.gate((_.C, _.NOT), (3, 2))
        handler.x += 0.7
        handler.gate((_.C, _.NOT), (2, 0))
        handler.x += 0.7
        handler.gate((_.C, _.NOT), (3, 2))
        handler.x += 1
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
            plt.text(*handler.get_position(i, x=-0.5), r'$\left\vert0\right\rangle_{Q_%d}$' %
                     i, va='center', ha='center', fontsize=18)


if __name__ == '__main__':
    ghz4()
