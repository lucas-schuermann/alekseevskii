__author__ = 'Lucas Schuermann'

from blocking.blocking import BlockingAlgorithm, BlockingAlgorithmSerial
from evaluation.evaluation import EvaluationAlgorithm, EvaluationAlgorithmSerial

#####
#
#
#####


class Manager:
    implementation_choices = ["Serial", "Serial (Cython)", "Multithreaded", "OpenCL"]

    def __init__(self):
        self.implementation = self.implementation_choices[0]
        self.blocker = BlockingAlgorithm
        self.blocks = None
        self.evaluator = EvaluationAlgorithm

    def set_implementation(self, implementation):
        self.implementation = implementation

    def setup_blocking(self):
        if self.implementation is self.implementation_choices[0]:
            print "Setting up", self.implementation, "blocking algorithm"
            self.blocker = BlockingAlgorithmSerial()
        elif self.implementation is self.implementation_choices[1] or self.implementation_choices[2] \
                or self.implementation_choices[3]:
            print "Not yet implemented:", self.implementation
        else:
            print "Invalid implementation choice:", self.implementation

    def run_blocking(self):
        self.blocks = self.blocker.iterate()

    def setup_evaluation(self):
        self.evaluator = EvaluationAlgorithmSerial()

    def run_evaluation(self):
        return self.evaluator.iterate(self.blocks)
