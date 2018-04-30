import pdb, re
import numpy as np
import matplotlib.pyplot as plt

from . import NodeBrush, DynamicShow, QuantumCircuit, Pin

GATE = NodeBrush('qc.basic')
WIDE = NodeBrush('qc.wide')
C = NodeBrush('qc.C')
NC = NodeBrush('qc.NC', size = 'tiny')
NOT = NodeBrush('qc.NOT', size='small')
END = NodeBrush('qc.end')
MEASURE = NodeBrush('qc.measure')
CORSS = NodeBrush('qc.cross')
BOX = NodeBrush('qc.box')

GATEMAP = {'C':C, 'NC': NC, 'NOT': NOT, 'Measure':MEASURE, 'X':GATE, 'Y':GATE,
        'Z':GATE, 'H':GATE, 'Rot': WIDE, 'Rx': WIDE, 'Ry':WIDE, 'Rz':WIDE, 'End':END}

setting = {'fontsize':14, 'show_params':False}

def _text_width(obj):
    '''the width of a text object.'''
    return 0.5

def _parse_lines(linecode):
    linecode = linecode.strip(' ')
    res = re.match(r'(\d+):(\d+)', linecode)
    if res:
        return slice(int(res.group(1)), int(res.group(2)))
    else:
        return [int(i.strip(' ')) for i in linecode.split('&')]

def _parse_params(linecode):
    linecode = linecode.strip(' ')
    if linecode == '': return ''
    floats = [float(i.strip(' ')) for i in linecode.split('&')]
    return '\n'+', '.join(['%s'%p for p in floats])

def _as_list(line):
    if isinstance(line, slice):
        line = list(range(line.start, line.stop + 1))
    return list(np.atleast_1d(line))

def vizcode(handler, code):
    '''visualize a code'''
    code = code.strip(' ')
    offsetx = 0
    if code[-1] == ';':
        offsetx += 1.2
        code=code[:-1]
    code_list = [s.strip(' ') for s in code.split('--')]
    show_params = setting['show_params']

    commands, lines, texts = [], [], []
    for code in code_list:
        res = re.match(r'/(\w+)\((.*)\)', code)
        if not res:
            raise ValueError('Invalid Code %s'%code)
        command = res.group(1)
        args = res.group(2).split(',')
        line = _parse_lines(args.pop(0))

        if command in ['C', 'NC', 'X', 'Y', 'Z', 'H', 'NOT']:
            b = GATEMAP[command]
            # get line
            commands.append(b)
            lines.append(line)

            if command not in ['NOT', 'C', 'NC']:
                text = command
            else:
                text = ''
            texts.append(text)
            if len(args) != 0:
                raise ValueError('Incorrect Number of Parameters: %s'%code)

        elif command in ['Rx', 'Ry', 'Rz', 'Rot']:
            b = GATEMAP[command]
            text = command
            # get line
            commands.append(b)
            lines.append(line)

            # get parameters
            param_text = _parse_params(args.pop(-1))

            # get text
            if len(args) != 0:
                raise ValueError('Incorrect Number of Parameters: %s'%code)
            if show_params:
                text += param_text
            texts.append(text)
        elif command == 'G':
            lines.append(line)
            line = _as_list(line)
            nline = max(line) - min(line) + 1

            # get parameters
            param_text = _parse_params(args.pop(-1))

            # get text
            if len(args) == 0:
                raise ValueError('Not Enough Parameters for Gate: %s'%code)
            text = ','.join(args).strip(' ')
            if show_params:
                text += param_text
            texts.append(text)

            commands.append(BOX)

        elif command in ['Measure', 'End']:
            b = GATEMAP[command]
            line = _as_list(line)
            if len(line) == 1:
                commands.append(b)
                texts.append('')
                lines.extend(line)
            else: # multiple measure can not support connection with other gates!
                for l in line:
                    handler.gate(b, l)
                handler.x += offsetx
                return
        elif command == 'Swap':
            commands.extend([CORSS]*2)
            if len(line)!=2:
                raise ValueError('Swap Gate Defintion Error: %s'%code)
            lines.extend(line)
            texts.extend(['']*2)
        elif command == 'Focus':
            handler.focus(_as_list(line))
            handler.x += offsetx
            return
        else:
            raise ValueError('Invalid Command %s'%command)
    print(commands, lines, texts)
    handler.gate(commands, lines, texts, fontsize=setting['fontsize'])
    handler.x += offsetx

def parsecircuit(datamap, handler=None):
    if handler is None: # top level
        num_bit = datamap['nline']
        handler = QuantumCircuit(num_bit=num_bit)

        # text |0>s
        for i in range(num_bit):
            plt.text(-0.4, -i, r'$\vert0\rangle$', va='center', ha='center', fontsize=setting['fontsize'])
        handler.x += 0.8

    if isinstance(datamap, str):
        vizcode(handler, datamap)
    else:
        for block in datamap['blocks']:
            parsecircuit(block, handler)
