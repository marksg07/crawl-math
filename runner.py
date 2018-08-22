from random import randint
import numpy as np
from discrete import uniform_discdist
symsets = ['d', '+-', 'x', '>']
syms = ''.join(symsets)
inp = '0x3d25-1d26+1'

def parse_exp(inp):
    sym_list = []
    buf = ''
    for a in inp:
        if a in syms:
            if '.' in buf:
                sym_list.append(float(buf))
            else:
                sym_list.append(int(buf))
            sym_list.append(a)
            buf = ''
        else:
            buf += a
    if '.' in buf:
        sym_list.append(float(buf))
    else:
        sym_list.append(int(buf))
    before = sym_list
    grouped = []
    noop = chr(2)
    for symset in symsets:
        i = 0
        print before, symset
        while i < len(before):
            window = before[i:i+3]
            #print 'window is', window
            if len(window) == 3 and isinstance(window[1], str) and window[1] in symset:
                before[i] = (before[i+1], before[i], before[i+2])
                #print i, before
                del before[i+1]
                del before[i+1]
                #print 'just deleted, im', before
                i -= 1
            #if isinstance(before[i], str) and before[i] in symset:
            #    grouped.append((before[i], before[i-1], before[i+1]))
            #    i += 2
            #else:
            #    grouped.append(before[i-1])
            i += 1
        #if i == len(before):
        #    grouped.append(before[-1])
        #before = grouped
        #grouped = []
    print before
    assert(len(before) == 1)
    return before[0]

def dice(n, d):
    '''s = 0
    for i in range(n):
        s += randint(1, d)'''
    s = uniform_discdist(1, d)
    for i in range(1, n):
        s += uniform_discdist(1, d)
    return s

def add(a, b):
    return a + b

def sub(a, b):
    return a + -b

def gt(a, b):
    return a > b

def mx(a, b):
    if isinstance(a, float) or isinstance(a, int):
        b.max(a)
        ret = b
    else:
        a.max(b)
        ret = a
    return ret

operations = {'d': dice, '+': add, '-': sub, 'x': mx, '>': gt}

def evalexp(exp):
    # first pass
    l2 = []
    op = exp[0]
    p1 = exp[1]
    p2 = exp[2]
    if isinstance(p1, tuple):
        p1 = evalexp(p1)
    if isinstance(p2, tuple):
        p2 = evalexp(p2)
    return operations[op](p1, p2)


if __name__ == '__main__':
    #inp = raw_input('Number of passes (default 100000): ').strip()
    #if inp == '':
    #    p = 100000
    #else:
    #    p = int(inp)
    inp = raw_input('Enter expression: ')
    exp = parse_exp(inp)
    print exp
    dist = evalexp(exp)
    print dist.expected()
    dist.graph()
    import matplotlib.pyplot as plt
    plt.show()
    '''s = 0
    for i in range(p):
        s += eval_once(exp)
    s /= 1. * p
    print s'''
