import matplotlib.pyplot as plt
from viznet import NodeBrush, DynamicShow, QuantumCircuit


def ghz4():
    '''4 bit GHZ circuit, applicable on ibmqx4 circuit.'''
    num_bit = 4
    with DynamicShow((5, 3), '_exact_ghz4_circuit.pdf') as ds:
        basic = NodeBrush('qc.basic', ds.ax)
        C = NodeBrush('qc.C', ds.ax)
        NOT = NodeBrush('qc.NOT', ds.ax, size='small')
        END = NodeBrush('qc.end', ds.ax)
        M = NodeBrush('qc.measure', ds.ax)

        handler = QuantumCircuit(num_bit=4)
        handler.x += 0.5
        handler.gate(basic, 0, 'X')
        for i in range(1, num_bit):
            handler.gate(basic, i, 'H')
        handler.x += 1
        handler.gate((C, NOT), (1, 0))
        handler.gate((C, NOT), (3, 2))
        handler.x += 0.7
        handler.gate((C, NOT), (2, 0))
        handler.x += 0.7
        handler.gate((C, NOT), (3, 2))
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
