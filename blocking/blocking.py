__author__ = 'Lucas Schuermann'

from time import time
import math
import numpy as np


class BlockingAlgorithm:
    def __init__(self):
        self.blocks = list()
        self.side_length = 1.0
        self.sphere_bound = math.sqrt(90.)/2.*self.side_length
        self.epsilon = 1.0e-10
        self.num_checked = 0

    def iterate(self):
        pass


def ind(i, j, k):
    return int((j-i)+5+5*(i-2)-(1.0/2.0)*(i-1)*(i-2)+15*(k-1)-1)


class BlockingAlgorithmSerial(BlockingAlgorithm):
    def __init__(self):
        BlockingAlgorithm.__init__(self)

    def _object_condition(self, block):
        # find min and max on block
        blkmin = np.array([0.0]*90)
        blkmax = np.array([0.0]*90)
        for i in range(90):
            blkmin[i] = block[i] - self.side_length
            blkmax[i] = block[i] + self.side_length

        def get_min(i, j, k):
            if i <= 6 and j <= 6 and k <= 6 and i < j:
                assert(0 <= ind(i,j,k) <= 89)
                return blkmin[ind(i, j, k)]
            return 0.0

        def get_max(i, j, k):
            if i <= 6 and j <= 6 and k <= 6 and i < j:
                assert(0 <= ind(i,j,k) <= 89)
                return blkmax[ind(i, j, k)]
            return 0.0

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

        def poly_min_max(terms, i, j, k, l, m=None):
            vars = [i, j ,k, l, m]

            def term(expr):
                if type(expr) is not float:
                    argcnt = 0
                    args = [0, 0, 0]
                    for exprcnt in range(3):
                        args[argcnt] = vars[expr[exprcnt]]
                        argcnt += 1
                    return get_min(args[0], args[1], args[2]), get_max(args[0], args[1], args[2])
                else:
                    return expr, expr

            for t in terms:
                print t
                out = 1.0
                for i in t:
                    val = term(i)
                    if val[0] < val[1]:
                        pass

        # jacobi condition
        # i=0, j=1, k=2, l=3, m=4
        jacterms = (((1, 2, 4), (4, 2, 3)), ((1, 2, 4), (4, 0, 3)), ((2, 0, 4), (4, 1, 3)))

        for k in range(1, 7):
            for i in range(1, 7):
                for j in range(i+1, 7):
                    jacmin = jacmax = 0.0
                    for l in range(1, 7):
                        for m in range(1, 7):
                            # TODO: min and max by term of this poly also? n
                            # note that multiple neg terms can result in positive answer that mimics that of the maximum
                            #jacmin += get_min(i, j, m)*get_min(m, k, l)+get_min(j, k, m)*get_min(m, i, l) \
                            #    + get_min(k, i, m)*get_min(m, j, l)
                            #jacmax += get_max(i, j, m)*get_max(m, k, l)+get_max(j, k, m)*get_max(m, i, l) \
                            #    + get_max(k, i, m)*get_max(m, j, l)
                            rmin, rmax = poly_min_max(jacterms, i, j, k, l, m)
                            jacmin += rmin
                            jacmax += rmax
                    if not jacmin <= 0. <= jacmax:
                        return False

        # einstein condition
        # i=0, j=1, k=2, l=3
        einterms = ((-1./2., (0, 2, 3), (1, 2, 3)), ((-1/2), (1, 2, 3), (0, 3, 2)), ((1/4), (2, 3, 0), (2, 3, 1)))

        def ric(i, j):
            smin = 0.0
            smax = 0.0
            for k in range(1, 7):
                for l in range(1, 7):
                    # TODO: min and max of these polynomials depending on value of variable
                    #smin += - (1./2.)*get_min(i, k, l)*get_min(j, k, l) - (1./2.)*get_min(j, k, l)*get_min(i, l, k) \
                    #    + (1./4.)*get_min(k, l, i)*get_min(k, l, j)
                    #smax += - (1./2.)*get_max(i, k, l)*get_max(j, k, l) - (1./2.)*get_max(j, k, l)*get_max(i, l, k) \
                    #    + (1./4.)*get_max(k, l, i)*get_max(k, l, j)
                    rmin, rmax = poly_min_max(einterms, i, j, k, l)
                    smin += rmin
                    smax += rmax
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

    def _add_blocks_from(self, b0):
        print "iterating over", b0
        for side in range(180):
            delta = np.array([0.0]*90)
            if side < 90:
                delta[side] = self.side_length
            else:
                delta[side - 90] = -self.side_length
            print "testing", b0 + delta, "..."
            self.num_checked += 1
            if self._object_condition(b0 + delta):
                if not self._redundant(b0 + delta):
                    self.blocks.append(b0 + delta)
                    print "added"
                else:
                    print "rejected"
            else:
                print "rejected"

    def _redundant(self, block):
        for b in self.blocks:
            if b.x-self.epsilon <= block.x <= b.x+self.epsilon:
                return True
        return False

    @staticmethod
    def _print_blocks(blocks):
        print "current blocks:"
        for b in blocks:
            print str(b)
        print "\n"

    def iterate(self):
        start = np.array([0.0]*90)
        start[ind(1,2,3)] = start[ind(1,3,2)] = start[ind(4,6,5)] = start[ind(4,5,6)] = 1.0/math.sqrt(6.0)
        start[ind(2,3,1)] = start[ind(5,6,4)] = -1.0/math.sqrt(6.0)
        self.blocks.append(start)
        checked = 0

        # TODO: fails jacobi condition
        print "START BLOCK CONDITION:", self._object_condition(start)

        while True:
            if checked >= len(self.blocks):
                break
            else:
                b = self.blocks[checked]
                self._add_blocks_from(b)
                self._print_blocks(self.blocks)
                checked += 1
        return self.blocks

if __name__ == '__main__':
    blocker = BlockingAlgorithmSerial()

    t0 = time()
    output = blocker.iterate()
    tf = time()

    elapsed = tf - t0
    print "elapsed time:", elapsed, "seconds"
    print "blocks used:", len(output)
    print "blocks checked:", blocker.num_checked
    print "avg time per block:", elapsed/blocker.num_checked, "seconds"