import numpy as np
import matplotlib.pyplot as plt
from sys import stdin


def test1():
    plt.rcParams['toolbar'] = 'None'
    ax = plt.subplot(111)

    t = np.arange(0.0, 5.0, 0.01)
    s = np.cos(2 * np.pi * t)
    line, = plt.plot(t, s, lw=2)

    plt.annotate('max', xy=(2, 1), xytext=(3, 1.5), arrowprops=dict(facecolor='black', shrink=0.05),)

    plt.ylim(-2, 2)
    plt.show()

if __name__ == "__main__":
    print "select test"
    test = int(stdin.readline())
    print test
    if test == 0:
        test1()
    else:
        print "No valid test index selected. Exiting..."