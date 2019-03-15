import numpy as np
import matplotlib.pyplot as plt
from viznet import DynamicShow, QuantumCircuit
from viznet import parsecircuit as _


def grover():
    num_bit = 5
    niter = 2
    _.BOX.size=(0.8, 0.3)
    with DynamicShow((10, 3.5), '_grover.png') as ds:
        handler = QuantumCircuit(num_bit=num_bit, y0=2., locs=-0.8*np.arange(num_bit))
        handler.x -= 0.8
        with handler.block(slice(0, num_bit-1), pad_x=0.2, pad_y=0.2) as boxes:
            handler.x += 2.0
            handler.gate(_.BOX, slice(0,num_bit), '$U$')
            handler.x += 0.5
        boxes[0].text("A", 'top')
        handler.x += 1.5
        with handler.block(slice(0, num_bit-1), pad_x=0.2, pad_y=0.2) as boxes:
            handler.x+=0.5
            handler.gate(_.BOX, slice(0,num_bit), r'oracle', fontsize=14)
            handler.x+=1.5
            with handler.block(slice(0, num_bit-1), pad_x=0.1, pad_y=0.1) as bxs:
                handler.x+=0.5
                handler.gate(_.BOX, slice(0,num_bit), r'$U^\dagger$')
                handler.x += 1.5
                handler.gate([_.NC]*(num_bit-1)+[_.WIDE], range(num_bit), ['']*(num_bit-1)+['-Z'])
                handler.x += 1.5
                handler.gate(_.BOX, slice(0,num_bit), '$U$')
                handler.x+=0.5
            bxs[0].text('B', 'top')
        boxes[0].text('C', 'top')
        handler.x+=2.0
        for i in range(niter-1):
            handler.gate(_.BOX, slice(0,num_bit), r'oracle', fontsize=14)
            handler.x+=2.0
            handler.gate(_.BOX, slice(0,num_bit), r'$U^\dagger$')
            handler.x += 1.5
            handler.gate([_.NC]*(num_bit-1)+[_.WIDE], range(num_bit), ['']*(num_bit-1)+['-Z'])
            handler.x += 1.5
            handler.gate(_.BOX, slice(0,num_bit), '$U$')
            handler.x+=2.5
        handler.x -=0.8
        for i in range(num_bit):
            handler.gate(_.END, i)

        # text |0>s
        for i in range(num_bit):
            plt.text(*handler.get_position(i, x=-0.5), r'$\left\vert 0\right\rangle_{Q_%d}$' %
                     (i+1), va='center', ha='center', fontsize=16)
        plt.text(8.5, -4.2, "Grover Search Circuit", ha='center')


if __name__ == '__main__':
    grover()
