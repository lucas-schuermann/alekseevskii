__author__ = 'Lucas Schuermann'

from time import time
import math


class Vector:
    def __init__(self, val=[0.] * 90):
        self.x = val

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self.x, other.x)])

    def __getitem__(self, item):
        return self.x[item]

    def __setitem__(self, key, value):
        self.x[key] = value

    def __str__(self):
        return str(self.x)


# TODO: check if value is valid
def ind(i, j, k):
    ret = (j-i)+5+5*(i-2)-(1/2)*(i-1)*(i-2)+16*(k-1)
    assert(0 <= ret <= 89)
    return ret

class BlockingAlgorithm:
    def __init__(self):
        self.blocks


class BlockingAlgorithmSerial:
    def __init__(self):
        self.blocks = list()
        self.side_length = 1.
        self.sphere_bound = math.sqrt(90.)/2.*self.side_length

    def object_condition(self, block):
        # find min and max on block
        blkmin = Vector()
        blkmax = Vector()
        for i in range(90):
            blkmin[i] = block[i] + self.side_length
            blkmax[i] = block[i] - self.side_length

        def get_min(i, j, k):
            if i <= 6 and j <= 6 and k <= 6 and i < j:
                print i, j, k
                print ind(i, j, k)
                return blkmin[ind(i, j, k)]

        def get_max(i, j, k):
            if i <= 6 and j <= 6 and k <= 6 and i < j:
                return blkmax[ind(i, j, k)]

        # unimodular condition
        unimin = 0.0
        unimax = 0.0
        for i in range(1, 7):
            for j in range(i+1, 7):
                unimin += get_min(i, j, j)
                unimax += get_max(i, j, j)
        if not unimin <= 0. <= unimax:
            return False

        # sphere condition
        s = 0.0
        b = self.sphere_bound
        for i in range(90):
            s += block[i]**2
        m = math.sqrt(s)
        if not (m - b) <= 1.0 <= (m + b):
            return False

        # jacobi condition
        for k in range(1, 7):
            for i in range(1, 7):
                for j in range(i+1, 7):
                    jacmin = jacmax = 0.0
                    for l in range(1, 7):
                        for m in range(1, 7):
                            jacmin += get_min(i, j, m)*get_min(m, k, l)+get_min(j, k, m)*get_min(m, i, l) \
                                + get_min(k, i, m)*get_min(m, j, l)
                            jacmax += get_max(i, j, m)*get_max(m, k, l)+get_max(j, k, m)*get_max(m, i, l) \
                                + get_max(k, i, m)*get_max(m, j, l)
                    if not jacmin <= 0. <= jacmax:
                        return False

        def poly_min_max(i, j, k, l):
            def term(expr):
                if type(expr) is not float:
                    for e in range(3):
                        if expr[e] is 0:
                            expr[e] = i
                        elif expr[e] is 1:
                            expr[e] = j
                        elif expr[e] is 2:
                            expr[e] = k
                        elif expr[e] is 3:
                            expr[e] = l
                    return get_min(expr[0], expr[1], expr[2]), get_max(expr[0], expr[1], expr[2])
                else:
                    return expr, expr

            # i=0, j=1, k=2, l=3
            terms = ((-1./2., (0, 2, 3), (1, 2, 3)), ((-1/2), (1, 2, 3), (0, 3, 2)), ((1/4), (2, 3, 0), (2, 3, 1)))
            for t in terms:
                print t
                out = 1.0
                for i in t:
                    val = term(i)
                    if val[0] < val[1]:
                        pass

        # einstein condition
        def ric(i, j):
            smin = 0.0
            smax = 0.0
            for k in range(1, 7):
                for l in range(1, 7):
                    # TODO: min and max of these polynomials depending on value of variable
                    smin += - (1./2.)*get_min(i, k, l)*get_min(j, k, l) - (1./2.)*get_min(j, k, l)*get_min(i, l, k) \
                        + (1./4.)*get_min(k, l, i)*get_min(k, l, j)
                    smax += - (1./2.)*get_max(i, k, l)*get_max(j, k, l) - (1./2.)*get_max(j, k, l)*get_max(i, l, k) \
                        + (1./4.)*get_max(k, l, i)*get_max(k, l, j)
            return smin, smax

        for i in range(1, 7):
            for j in range(1, 7):
                if i is not j:
                    ijmin, ijmax = ric(i, j)
                    iimin, iimax = ric(i, i)
                    jjmin, jjmax = ric(j, j)
                    if not ijmin <= 0. <= ijmax:
                        return False

                    # TODO: is this correct? should it be |ric{ii} - ric{jj}|?
                    if not (iimin - jjmin) <= 0. <= (iimax - jjmax):
                        return False

    def add_blocks_from(self, b0):
        print "iterating over", b0
        for side in range(180):
            delta = Vector()
            if side < 90:
                delta[side] = self.side_length
            else:
                delta[side - 90] = -self.side_length
            print "testing", b0 + delta, "..."
            if self.object_condition(b0 + delta):
                if not self.redundant(b0 + delta):
                    self.blocks.append(b0 + delta)
                    print "added"
                else:
                    print "rejected"
            else:
                print "rejected"

    def redundant(self, block):
        for b in self.blocks:
            if block.x == b.x:
                return True
        return False

    @staticmethod
    def _print_blocks(blocks):
        print "current blocks:"
        for b in blocks:
            print str(b)
        print "\n"

    # TODO: create class for tracking data in real-time
    def iterate(self):
        start = Vector()
        start[ind(1, 2, 1)] = start[ind(1, 2, 2)] = start[ind(1, 3, 1)] = start[ind(1, 3, 3)] = start[ind(2, 3, 2)] \
            = start[ind(2, 3, 3)] = 0.
        start[ind(1, 2, 3)] = start[ind(1, 3, 2)] = 1.0 / math.sqrt(6.0)
        start[ind(2, 3, 1)] = - 1.0 / math.sqrt(6.0)
        print start

        self.blocks.append(start)
        checked = 0
        while True:
            if checked >= len(self.blocks):
                break
            else:
                b = self.blocks[checked]
                self.add_blocks_from(b)
                self._print_blocks(self.blocks)
                checked += 1
        return self.blocks

if __name__ == "__main__":
    blocker = BlockingAlgorithmSerial()

    start = Vector()
    start[ind(1, 2, 1)] = start[ind(1, 2, 2)] = start[ind(1, 3, 1)] = start[ind(1, 3, 3)] = start[ind(2, 3, 2)] \
        = start[ind(2, 3, 3)] = 0.
    start[ind(1, 2, 3)] = start[ind(1, 3, 2)] = 1.0 / math.sqrt(6.0)
    start[ind(2, 3, 1)] = - 1.0 / math.sqrt(6.0)
    print start
    print blocker.object_condition(start)

    #t0 = time()
    #output = blocker.iterate()
    #tf = time()

    #elapsed = tf - t0
    #print "elapsed time:", elapsed, "seconds"
    #print "blocks used:", len(output)