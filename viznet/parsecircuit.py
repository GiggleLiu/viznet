import pdb, re
import numpy as np
import matplotlib.pyplot as plt

from . import NodeBrush, DynamicShow, QuantumCircuit, Pin

GATE = NodeBrush('qc.basic')
WIDE = NodeBrush('qc.wide')
C = NodeBrush('qc.C')
NOT = NodeBrush('qc.NOT', size='small')
END = NodeBrush('qc.end')
MEASURE = NodeBrush('qc.measure')
CORSS = NodeBrush('qc.cross')

GATEMAP = {'C':C, 'NOT': NOT, 'Measure':MEASURE, 'X':GATE, 'Y':GATE,
        'Z':GATE, 'H':GATE, 'G': WIDE, 'Rot': WIDE, 'Rx': WIDE, 'Ry':WIDE, 'Rz':WIDE, 'End':END}

def _text_width(obj):
    '''the width of a text object.'''
    return 1

def _parse_lines(linecode):
    linecode = linecode.strip(' ')
    res = re.match(r'(\d+):(\d+)', linecode)
    if res:
        return slice(int(res.group(1)), int(res.group(2)))
    else:
        return [int(i.strip(' ')) for i in linecode.split('&')]

def _parse_params(command, linecode):
    linecode = linecode.strip(' ')
    return [float(i.strip(' ')) for i in linecode.split('&')]

def vizcode(handler, code, show_params=True):
    '''visualize a code'''
    code = code.strip(' ')
    offsetx = 0
    if code[-1] == ';':
        offsetx += 0.8
        code=code[:-1]
    code_list = [s.strip(' ') for s in code.split('--')]

    commands, lines, texts = [], [], []
    for code in code_list:
        res = re.match(r'/(\w+)\((.*)\)', code)
        if not res:
            raise ValueError('Invalid Code %s'%code)
        command = res.group(1)
        args = res.group(2).split(',')
        line = _parse_lines(args.pop(0))

        if command in ['C', 'X', 'Y', 'Z', 'H', 'NOT']:
            b = GATEMAP[command]
            # get line
            commands.append(b)
            lines.append(line)

            if command not in ['NOT', 'C']:
                text = command
            else:
                text = ''
            texts.append(text)
            if len(args) != 0:
                raise ValueError('Incorrect Number of Parameters: %s'%code)

        elif command in ['Rx', 'Ry', 'Rz', 'Rot', 'G']:
            b = GATEMAP[command]
            # get line
            commands.append(b)
            lines.append(line)

            # get parameters
            params = _parse_params(args.pop(-1))
            param_text = '\n'+', '.join('%s'%params)

            # get text
            if command == 'G':
                if len(args) == 0:
                    raise ValueError('Not Enough Parameters for Gate: %s'%code)
                text = ','.join(args).strip(' ')
                # adjust width according to text
                b.size = (b.size, b.size*_text_width(text))
            else:
                if len(args) != 0:
                    raise ValueError('Incorrect Number of Parameters: %s'%code)
            if show_params:
                text += param_text

        elif command in ['Measure', 'End']:
            b = GATEMAP[command]
            if isinstance(line, slice):
                line = list(range(line.start, line.stop))
            line = np.atleast_1d(line)
            for l in line:
                handler.gate(b, l)
            return
        elif command == 'SWAP':
            commands.extend([CORSS]*2)
            if len(line)!=2:
                raise ValueError('Swap Gate Defintion Error: %s'%code)
            lines.extend(line)
            texts.append(['']*2)
        else:
            raise ValueError('Invalid Command %s'%command)
    print(commands, lines, texts)
    handler.gate(commands, lines, texts)
    handler.x += offsetx

def parsecircuit(datamap):
    num_bit = datamap['nline']
    handler = QuantumCircuit(num_bit=num_bit)

    with DynamicShow() as ds:
        handler.x += 0.5
        handler.gate(basic, 0, 'X')
        for i in range(1, num_bit):
            handler.gate(basic, i, 'H')
        handler.x += 1
        handler.gate((C, NOT), (1, 0))
        handler.gate((C, NOT), (3, 2))
    BOX = handler.boxbrush(nline)

    handler.x += 0.7
    handler.gate((C, NOT), (2, 0))
    handler.x += 0.7
    handler.gate((C, NOT), (3, 2))
    handler.x += 1
    for i in range(num_bit):
        handler.gate(basic, i, 'H')
    handler.x += 1
    handler.gate(BOX, slice(0, 4), '$e^{-iHt}$')
    handler.x += 1
    for i in range(num_bit):
        handler.gate(M, i)
    handler.edge.ls = '='
    handler.x += 0.8
    for i in range(num_bit):
        handler.gate(END, i)

    # text |0>s
    for i in range(num_bit):
        plt.text(-0.4, -i, r'$\vert0\rangle_{Q_%d}$' %
                 i, va='center', ha='center', fontsize=18)



def blockfocus():
    '''illustration of block-focus scheme.'''
    num_bit = 6
    with DynamicShow((5, 3), '_blockfocus.png') as ds:
        block = NodeBrush('box', size=(2, 2), ls='--', roundness=0.2)

        handler = QuantumCircuit(num_bit=num_bit)
        handler.x += 0.8
        handler.gate(basic, 0, 'X')
        for i in range(1, num_bit):
            handler.gate(basic, i, 'H')
        handler.x += 0.8
        with handler.block(block, 0, num_bit-1, pad_x=0.1) as b:
            handler.focus([4, 2, 1, 3])
        b[0].text('focus', 'top')
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
            plt.text(-0.5, -i, r'$\left\vert0\right\rangle$'
                     , va='center', ha='center', fontsize=16)


if __name__ == '__main__':
    blockfocus()
