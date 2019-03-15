import matplotlib.pyplot as plt
from viznet import DynamicShow, QuantumCircuit
from viznet import parsecircuit as _


def qft():
    num_bit = 5
    with DynamicShow((10, 3.5), '_qft.png') as ds:
        handler = QuantumCircuit(num_bit=num_bit, y0=2.)
        handler.x += 0.7
        for i in range(num_bit):
            if i ==1:
                context = handler.block(slice(i, num_bit-1), pad_y=0.1, pad_x=0.2)
                boxes = context.__enter__()
            for k in range(i, num_bit):
                if i==k:
                    handler.gate(_.GATE, i, 'H')
                else:
                    if i ==0 and k==1+2:
                        context = handler.block(slice(i, k), pad_y=0.1, pad_x = 0.15)
                        boxes = context.__enter__()
                    handler.gate((_.C, _.WIDE), (k, i), ['',r'R${}_%d$'%(k-i+1)])
                    if i ==0 and k==1+2:
                        context.__exit__(None, None, None)
                        boxes[0].text("A", "top")
                if i==1 and k==num_bit-1:
                    context.__exit__(None, None, None)
                    boxes[0].text("B", "top")
                handler.x+=1.0
            handler.x+=0.2
        for i in range(num_bit):
            handler.gate(_.END, i)

        # text |0>s
        for i in range(num_bit):
            plt.text(*handler.get_position(i, x=-0.5), r'$\left\vert ?\right\rangle_{Q_%d}$' %
                     (i+1), va='center', ha='center', fontsize=16)
        plt.text(8.5, -3, "Quantum Fourier Transformation circuit of size 5", ha='center')


if __name__ == '__main__':
    qft()
