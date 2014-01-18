__author__ = 'Lucas Schuermann'

from blocking.blocking import BlockingAlgorithmSerial


class Manager:
    implementation_choices = ["Serial", "Serial (Cython)", "Multithreaded", "OpenCL"]

    def __init__(self):
        self.implementation = self.implementation_choices[0]
        self.blocker = None

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
        self.blocker.iterate()
