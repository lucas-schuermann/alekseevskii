__author__ = 'Lucas'

from time import time


class Vector:
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, val):
        return Point(self[0] + val[0], self[1] + val[1])

    def __sub__(self, val):
        return Point(self[0] - val[0], self[1] - val[1])

    def __iadd__(self, val):
        self.x = val[0] + self.x
        self.y = val[1] + self.y
        return self

    def __isub__(self, val):
        self.x = self.x - val[0]
        self.y = self.y - val[1]
        return self

    def __div__(self, val):
        return Point(self[0] / val, self[1] / val)

    def __mul__(self, val):
        return Point(self[0] * val, self[1] * val)

    def __idiv__(self, val):
        self[0] = self[0] / val
        self[1] = self[1] / val
        return self

    def __imul__(self, val):
        self[0] = self[0] * val
        self[1] = self[1] * val
        return self

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise Exception("Invalid key to Point")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise Exception("Invalid key to Point")

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
Point = Vector


class AlgorithmTest:
    def __init__(self):
        self.blocks = list()
        self.side_length = 1.0

    def object_condition(self, block):
        """x^2+y^2<1"""
        flag = False
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                x = block[0] + i * self.side_length
                y = block[1] + j * self.side_length
                if x ** 2 + y ** 2 < 1:
                    flag = True
        return flag

    def add_blocks_from(self, b0):
        print "iterating over", b0
        for side in range(4):
            delta = Vector()
            if side < 2:
                delta[side] = self.side_length
            else:
                delta[side - 2] = -self.side_length
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
            if block.x == b.x and block.y == b.y:
                return True
        return False

    @staticmethod
    def _print_blocks(blocks):
        print "current blocks:",
        for b in blocks:
            print str(b),
        print "\n"

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
    print "test condition:", test.object_condition.__doc__
    print "starting block:", test.iterate.__doc__
    print "side length:", test.side_length, "\n"

    start = time()
    output = test.iterate()
    end = time()

    elapsed = end - start
    print "elapsed time:", elapsed, "seconds"
    print "blocks used:", len(output)