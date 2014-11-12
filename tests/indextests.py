__author__ = 'Lucas Schuermann'

import timeit

import pyximport; pyximport.install()
import cythontests

# python vs Cython for the object condition, and testing various implementation to find the quickest
# was to obtain the index in a vector from the mu i mu j and mu k


def ind(i, j, k):
    return int((j-i)+5+5*(i-2)-(1./2.)*(i-1)*(i-2)+15*(k-1))

if __name__ == "__main__":
    num = 500000
    t = timeit.Timer("indextests.ind(%d,%d,%d)" % (1,1,1), "import indextests")
    print "Pure python function", t.timeit(num), "sec"
    t = timeit.Timer("cythontests.ind(%d,%d,%d)" % (1,1,1), "import pyximport; pyximport.install(); import cythontests")
    print "Cython function no cast", t.timeit(num), "sec"
    t = timeit.Timer("int(cythontests.ind(%d,%d,%d))" % (1,1,1), "import pyximport; pyximport.install(); import cythontests")
    print "Cython function with Python type cast", t.timeit(num), "sec"
    t = timeit.Timer("cythontests.ind2(%d,%d,%d)" % (1,1,1), "import pyximport; pyximport.install(); import cythontests")
    print "Cython function with cast", t.timeit(num), "sec"

    print ind(1,1,1)
    print cythontests.ind(1,1,1)
    print int(cythontests.ind(1,1,1))
    print cythontests.ind2(1,1,1)

# Results (avg execution time @ 500000 iterations, in seconds)
#
# Pure: 0.45526599884
# Cython no cast: 0.0767078399658
# Cython pycast: 0.155315876007
# Cython cast: 0.136200904846
#
# Fastest: Cython pycast, since a cast must be included