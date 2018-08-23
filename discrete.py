import matplotlib.pyplot as plt

sum_lim = 2**63-1
div = 2**16

    
'''
    def __neg__(self):
        def op(a, _):
            return BoundedDiscreteDistribution({-a:1})
        return self.apply_op(op, BoundedDiscreteDistribution({0:1})

    def __add__(self, other):
        def op(a, b):
            return BoundedDiscreteDistribution({a+b:1})
        return self.apply_op(op, other)
    
    def max(self, other):
        def op(a, b):
            return BoundedDiscreteDistribution({max(a, b): 1})
        return self.apply_op(op, other)

    def __gt__(self, other):
        def op(a, b):
            if a > b:
                return BoundedDiscreteDistribution({1:1})
            else:
                return BoundedDiscreteDistribution({0:1})
        return self.apply_op(op, other)
'''

class BoundedDiscreteDistribution:
    def __init__(self, pmf):
        self.pmf = pmf
        self.sum = sum(pmf.values())

    def apply_op(self, op, b):
        a = self # yes, i'm lazy
        newsum = 0
        newpmf = {}
        for i, iw in a.pmf.iteritems():
            for j, jw in b.pmf.iteritems():
                op_dis = op(i, j)
                for k, kw in op_dis.pmf.iteritems():
                    if k in newpmf:
                        newpmf[k] += iw*jw*kw
                    else:
                        newpmf[k] = iw*jw*kw
                    newsum += iw*jw*kw
        while newsum > sum_lim:
            newsum //= div # approx
            for k in newpmf.keys():
                v = newpmf[k]
                if v < div:
                    del newpmf[k]
                else:
                    newpmf[k] //= div
        return BoundedDiscreteDistribution(newpmf)

    def intize(self):
        def op(a, _): # 5.2, f = 0.2 
            floating = a - int(a)
            f_prob = int(floating * div)
            return BoundedDiscreteDistribution({int(a): div - f_prob, int(a)+1: f_prob})
        return self.apply_op(op, BoundedDiscreteDistribution({0: 1}))

    def graph(self):
        x = sorted(self.pmf.keys())
        y = [self.pmf[i] for i in x]
        plt.plot(x, y)
        plt.ylim(ymin=0)

    def expected(self):
        #print self.sum, sum(self.pmf.values())
        s_e = 0.
        for i,j in self.pmf.iteritems():
            s_e += i*j
        return s_e / self.sum

    def __str__(self):
        return str(self.pmf)

    def norm_weights_to(self, n):
        newpmf = {}
        mult = float(n) / self.sum
        for k in self.pmf.keys():
            newpmf[k] = self.pmf[k] * mult
        return BoundedDiscreteDistribution(newpmf)
            
def uniform_discdist(lo, hi):
    if hi < lo:
        return BoundedDiscreteDistribution({0:1})
    return BoundedDiscreteDistribution({i:1 for i in range(lo, hi+1)})

if __name__ == '__main__':
    d25 = uniform_discdist(1, 25)
    acroll = uniform_discdist(-25, 0)
    final = d25 + d25 + d25 + acroll
    final.max(0)
    kills = final > 29
    print kills.expected()
    print final.expected()
    final.graph()
    plt.show()
