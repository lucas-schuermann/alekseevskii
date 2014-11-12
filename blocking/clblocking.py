__author__ = 'Lucas Schuermann'

from blocking.blocking import BlockingAlgorithm

# to be extended to a blocking algorithm implemented with an OpenCL backend


class BlockingAlgorithmOpenCL(BlockingAlgorithm):
    def __init__(self):
        BlockingAlgorithm.__init__(self)