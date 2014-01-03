__author__ = 'Lucas'

from time import time
import random


class Vector:
    """90 dimensional vector"""
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


class DataStream:
    def __init__(self):
        self.vars = list()


class AlgorithmTest:
    def __init__(self):
        self.blocks = list()
        self.side_length = 1.0
        self.polys_deg1 = list()
        self.polys_deg2 = list()
        self.epsilon = 0.000001
        random.seed(1996)

    @staticmethod
    def _generate_coeffs(order):
        coeffs = list()
        for i in range(90 * order):
            coeffs.append(random.uniform(-1.0, 1.0))
        return coeffs

    def generate_polys(self):
        for i in range(45):
            self.polys_deg1.append(self._generate_coeffs(1))
        for i in range(44):
            self.polys_deg2.append(self._generate_coeffs(2))

    def print_polys(self):
        print "condition polynomial coeffs:"
        for i in range(len(self.polys_deg1)):
            print self.polys_deg1[i]
        for i in range(len(self.polys_deg2)):
            print self.polys_deg2[i]
        print "\n"

    def check_polys(self, position):
        ret = True
        for i in range(len(self.polys_deg1)):
            polyval = 0.
            for j in range(90):
                polyval += self.polys_deg1[i][j]*position.x[j]
            if not abs(polyval) < self.epsilon:
                ret = False
        for i in range(len(self.polys_deg2)):
            polyval = 0.
            for j in range(180):
                if j < 90:
                    polyval += self.polys_deg2[i][j]*position.x[j]
            else:
                    polyval += self.polys_deg2[i][j]*position.x[j-90]**2
            if not abs(polyval) < self.epsilon:
                ret = False
        return ret

    def find_min_max(self, block):

        return 0, 0

    def object_condition(self, block):
        flag = False
        side = self.side_length

        pos1, pos2 = self.find_min_max(block)
        if self.check_polys(block):
            flag = True

        return flag

    def add_blocks_from(self, b0):
        print "iterating over", b0
        for side in range(180):
            delta = Vector()
            if side < 90:
                delta[side] = self.side_length
            else:
                delta[side - 90] = -self.side_length
            print "testing", b0 + delta, "...",
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
        print "current blocks:",
        for b in blocks:
            print str(b),
        print "\n"

    # TODO: create class for tracking data in real-time
    def iterate(self):
        """start = (0.0, 0.0)"""
        starting_block = Vector()
        self.blocks.append(starting_block)
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
    test = AlgorithmTest()

    test.generate_polys()
    test.print_polys()

    print "test condition:", test.object_condition.__doc__
    print "starting block:", test.iterate.__doc__
    print "side length:", test.side_length, "\n"

    start = time()
    output = test.iterate()
    end = time()

    elapsed = end - start
    print "elapsed time:", elapsed, "seconds"
    print "blocks used:", len(output)