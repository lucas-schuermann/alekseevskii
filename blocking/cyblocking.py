# This file implements the blocking algorithm using Cython
#
# It is not complete, but the beginnings of an interface are here, along with a bit of optimized code
# The rest of the work could be fairly straightforward: simply identifying and declaring data types,
# then using C-based operations for the time-dependent calculations

from blocking import BlockingAlgorithm
import numpy
import math
from time import time

import pyximport
pyximport.install(setup_args={"include_dirs": numpy.get_include()},
                  reload_support=True)
import cyblocking_kernels
# see the index kernel implementation and methodology from the testing section
ind = cyblocking_kernels.ind_python


class BlockingAlgorithmCython(BlockingAlgorithm):
    def __init__(self):
        BlockingAlgorithm.__init__(self)

    def _object_condition(self, block):
        return cyblocking_kernels.object_condition(block, self.side_length,
                                                   self.sphere_bound)

    def _add_blocks_from(self, b0):
        print("iterating over", b0)
        for side in range(180):
            delta = numpy.array([0.0] * 90)
            if side < 90:
                delta[side] = self.side_length
            else:
                delta[side - 90] = -self.side_length
            print("testing", b0 + delta, "...")
            self.num_checked += 1
            if self._object_condition(b0 + delta):
                if not self._redundant(b0 + delta):
                    self.blocks.append(b0 + delta)
                    print("added")
                else:
                    print("rejected")
            else:
                print("rejected")

    def _redundant(self, block):
        for b in self.blocks:
            if numpy.array_equal(b, block):
                return True
        return False

    @staticmethod
    def _print_blocks(blocks):
        print("current blocks:")
        for b in blocks:
            print(str(b))
        print("\n")

    def iterate(self):
        start = numpy.array([0.0] * 90)
        start[ind(1, 2, 3)] = start[ind(1, 3,
                                        2)] = start[ind(4, 6, 5)] = start[ind(
                                            4, 5, 6)] = 1.0 / math.sqrt(6.0)
        start[ind(2, 3, 1)] = start[ind(5, 6, 4)] = -1.0 / math.sqrt(6.0)
        self.blocks.append(start)
        checked = 0

        # TODO: fails jacobi condition
        print("START BLOCK CONDITION:", self._object_condition(start))

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
    blocker = BlockingAlgorithmCython()

    t0 = time()
    output = blocker.iterate()
    tf = time()

    elapsed = tf - t0
    print("elapsed time:", elapsed, "seconds")
    print("blocks used:", len(output))
    print("blocks checked:", blocker.num_checked)
    print("avg time per block:", elapsed / blocker.num_checked, "seconds")
