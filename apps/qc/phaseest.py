import numpy as np
import matplotlib.pyplot as plt
import viznet
from viznet import DynamicShow, QuantumCircuit
from viznet import parsecircuit as _

def qft():
    num_bit = 5
    num_bit2 = 3
    with DynamicShow((7, 5), '_phaseest.png') as ds:
        handler = QuantumCircuit(num_bit=num_bit+num_bit2, y0=2., locs=-np.append(0.8*np.arange(num_bit), 0.9*num_bit+0.3*np.arange(num_bit2)))
        handler.x += 0.7
        with handler.block(slice(0, num_bit-1), pad_x=0.2, pad_y=0.2) as boxes:
            [handler.gate(_.GATE, i, 'H') for i in range(num_bit)]
        boxes[0].text("A", 'top')
        handler.x +=1.2
        _.BOX.size = (0.4, 0.3)
        with handler.block(slice(0, num_bit+num_bit2-1),pad_x=0.2, pad_y=0.2) as boxes:
            for i in range(num_bit):
                handler.gate((_.C, _.BOX), (i, slice(num_bit,num_bit+num_bit2-1)), ['', r'$U^{%d}$'%(2**i)])
                if i!=num_bit-1:
                    handler.x +=1.0
        boxes[0].text("B", 'top')
        handler.x +=0.7
        for i in range(num_bit2):
            handler.gate(viznet.NodeBrush('pin'), num_bit+i)
        handler.x +=0.7

        _.BOX.size = (0.6, 0.3)
        handler.gate(_.BOX, slice(0, num_bit-1), r'QFT${}^\dagger$')
        handler.x +=1.0
        for i in range(num_bit):
            handler.gate(_.END, i)

        # text |0>s
        for i in range(num_bit+num_bit2):
            plt.text(*handler.get_position(i, x=-0.5), r'$\left\vert %s\right\rangle_{Q_%d}$' %
                     (0 if i<num_bit else '?', i+1), va='center', ha='center', fontsize=16)
        plt.text(3.5, -6, "Quantum Circuit for Phase Estimation", ha='center')


if __name__ == '__main__':
    qft()
