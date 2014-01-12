__author__ = 'Lucas Schuermann'

from blocking import BlockingAlgorithmSerial


class Manager:
    implementation_choices = ["Serial", "Serial (Cython)", "Multithreaded", "OpenCL"]

    def __init__(self):
        self.implementation = self.implementation_choices[0]
        self.blocker = None

    def set_implementation(self, implementation):
        self.implementation = implementation

    def setup_blocking(self):
        if self.implementation is self.implementation_choices[0]:
            self.blocker = BlockingAlgorithmSerial()
        elif self.implementation is self.implementation_choices[1] or self.implementation_choices[2] \
                or self.implementation_choices[3]:
            print "Not yet implemented"
        else:
            print "Invalid implementation choice"

    def run_blocking(self):
        self.blocker.iterate()
