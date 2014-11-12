__author__ = 'Lucas Schuermann'

from blocking.blocking import BlockingAlgorithm

# To be a multithreaded implementation of the blocking algorithm, ideally running the object condition on blocks
# in parallel, including iterating to the next block to always keep the working set populated


class BlockingAlgorithmMultiThreaded(BlockingAlgorithm):
    def __init__(self):
        BlockingAlgorithm.__init__(self)