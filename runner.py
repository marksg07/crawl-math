from random import randint
#import numpy as np
from discrete import uniform_discdist, BoundedDiscreteDistribution

symsets = ['d', '*/', '+-', 'x', '>']
syms = ''.join(symsets) + ')('
inp = '0x3d25-1d26+1'

def dis_from_num(num):
    return BoundedDiscreteDistribution({num: 1})

def symlist(inp):
    sym_list = ['(']
    buf = ''
    for a in inp:
        if a in syms:
            #print(a, buf)
            if buf != '':
                if '.' in buf:
                    sym_list.append(dis_from_num(float(buf)))
                else:
                    #print(buf)
                    sym_list.append(dis_from_num(int(buf)))
            sym_list.append(a)
            buf = ''
        else:
            buf += a
    if buf != '':
        if '.' in buf:
            sym_list.append(dis_from_num(float(buf)))
        else:
            sym_list.append(dis_from_num(int(buf)))
    sym_list.append(')')
    return sym_list

def solve_parens(sym_list):
    # i'm lazy, one pass for each parens
    i = 0
    last_open = -1
    while i < len(sym_list):
        if sym_list[i] == '(':
            last_open = i
        elif sym_list[i] == ')':
            if last_open == -1:
                raise Exception('Invalid syntax: %s' % (' '.join(sym_list)))
            newexp = parse_exp(sym_list[last_open+1:i])
            sym_list = sym_list[:last_open] + [newexp] + sym_list[i+1:]
            i = -1
            last_open = -1
        i += 1
    assert(len(sym_list) == 1)
    return sym_list[0]
    

def parse_exp(sym_list):
    before = sym_list
    grouped = []
    noop = chr(2)
    for symset in symsets:
        i = 0
        #print before, symset
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
    #print before
    assert(len(before) == 1)
    return before[0]

def add(a, b):
    #print(a, b)
    return BoundedDiscreteDistribution({a+b:1})

def dice(n, d):
    #print(n, d)
    n_i = BoundedDiscreteDistribution({n:1}).intize()
    d_i = BoundedDiscreteDistribution({d:1}).intize()
    #print(str(n_i), str(d_i))
    def op(a, b):
        #print(a, b)
        s = BoundedDiscreteDistribution({0:1})
        for i in range(a):
            s = s.apply_op(add, uniform_discdist(1, b))
        return s.norm_weights_to(2**32)
    return n_i.apply_op(op, d_i)

def sub(a, b):
    return BoundedDiscreteDistribution({a-b:1})

def gt(a, b):
    if a > b:
        return BoundedDiscreteDistribution({1:1})
    return BoundedDiscreteDistribution({0:1})

def mx(a, b):
    return BoundedDiscreteDistribution({max(a,b):1})

def mul(a, b):
    return BoundedDiscreteDistribution({a*b:1})

def div(a, b):
    return BoundedDiscreteDistribution({a/float(b):1})

operations = {'d': dice, '+': add, '-': sub, 'x': mx, '>': gt, '*': mul, '/': div}

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
    return p1.apply_op(operations[op], p2)


if __name__ == '__main__':
    #inp = raw_input('Number of passes (default 100000): ').strip()
    #if inp == '':
    #    p = 100000
    #else:
    #    p = int(inp)
    inp = raw_input('Enter expression: ')
    inp = inp.replace(' ','').replace('\t', '').replace('\n', '').replace('\r', '')
    exp = solve_parens(symlist(inp))
    # print exp
    dist = evalexp(exp).intize()
    #print(dist)
    print 'Expected value:', dist.expected()
    #dist.graph()
    #import matplotlib.pyplot as plt
    #plt.show()
    '''s = 0
    for i in range(p):
        s += eval_once(exp)
    s /= 1. * p
    print s'''
