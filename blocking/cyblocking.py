__author__ = 'Lucas Schuermann'

from blocking.blocking import BlockingAlgorithm


class BlockingAlgorithmCython(BlockingAlgorithm):
    def __init__(self):
        BlockingAlgorithm.__init__(self)