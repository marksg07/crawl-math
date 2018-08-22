import matplotlib.pyplot as plt

sum_lim = 2**63-1
div = 2**16

class BoundedDiscreteDistribution:
    def __init__(self, pmf):
        self.pmf = pmf
        self.sum = sum(pmf.values())

    def __neg__(self):
        return BoundedDiscreteDistribution({-i:j for i,j in self.pmf.iteritems()})
        
    def __add__(self, other):
        if isinstance(other, int):
            return BoundedDiscreteDistribution({i+other:j for i,j in self.pmf.iteritems()})
        p1 = self.pmf
        p2 = other.pmf
        newsum = other.sum * self.sum
        p3 = {}
        for i,j in p1.iteritems():
            for i1,j1 in p2.iteritems():
                if i+i1 in p3:
                    p3[i+i1] += j * j1
                else:
                    p3[i+i1] = j * j1
        if newsum > sum_lim:
            for i in p3.keys():
                if p3[i] < div:
                    del(p3[i])
                else:
                    p3[i] /= div
        return BoundedDiscreteDistribution(p3)

    def __gt__(self, i):
        s = 0
        for k in self.pmf.keys():
            if k > i:
                s += self.pmf[k]
        n = self.sum - s
        return BoundedDiscreteDistribution({0: n, 1: s})

    def expected(self):
        #print self.sum, sum(self.pmf.values())
        s_e = 0.
        for i,j in self.pmf.iteritems():
            s_e += i*j
        return s_e / self.sum
    
    def max(self, i):
        #print i
        if i not in self.pmf:
            #print 'haha'
            self.pmf[i] = 0
        for k in self.pmf.keys():
            #print k
            if k < i:
                self.pmf[i] += self.pmf[k]
                del self.pmf[k]
    
    def graph(self):
        x = sorted(self.pmf.keys())
        y = [self.pmf[i] for i in x]
        plt.plot(x, y)

    def prob_gt(self, i):
        s = 0.
        for k in self.pmf.keys():
            if k > i:
                s += self.pmf[k]
        return s / self.sum
        

def uniform_discdist(lo, hi):
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
