# python vs Cython for the object condition, and testing various implementation to find the quickest
# was to obtain the index in a vector from the mu i mu j and mu k

import timeit
import pyximport
pyximport.install()
import cythontests


def ind(i, j, k):
    return int((j - i) + 5 + 5 * (i - 2) - (1. / 2.) * (i - 1) * (i - 2) + 15 *
               (k - 1))

if __name__ == "__main__":
    num = 500000
    t = timeit.Timer("indextests.ind(%d,%d,%d)" % (1, 1, 1),
                     "import indextests")
    print("Pure python function", t.timeit(num), "sec")
    t = timeit.Timer(
        "cythontests.ind(%d,%d,%d)" % (1, 1, 1),
        "import pyximport; pyximport.install(); import cythontests")
    print("Cython function no cast", t.timeit(num), "sec")
    t = timeit.Timer(
        "int(cythontests.ind(%d,%d,%d))" % (1, 1, 1),
        "import pyximport; pyximport.install(); import cythontests")
    print("Cython function with Python type cast", t.timeit(num), "sec")
    t = timeit.Timer(
        "cythontests.ind2(%d,%d,%d)" % (1, 1, 1),
        "import pyximport; pyximport.install(); import cythontests")
    print("Cython function with cast", t.timeit(num), "sec")

    print(ind(1, 1, 1))
    print(cythontests.ind(1, 1, 1))
    print(int(cythontests.ind(1, 1, 1)))
    print(cythontests.ind2(1, 1, 1))

# Results (avg execution time @ 500000 iterations, in seconds)
#
# Pure python function 0.21579052900000006 sec
# Cython function no cast 0.04513908499999997 sec
# Cython function with Python type cast 0.09326969099999993 sec
# Cython function with cast 0.04489870500000004 sec
#
# Fastest: Cython pycast
