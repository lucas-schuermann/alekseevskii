__author__ = 'Lucas Schuermann'

import math
import numpy as np
cimport numpy as np

# implement time-critical parts of the algorithm in Cython

# NOTE THIS IS NOT FINISHED, MANY CHANGES NEEDED

def ind_python(int i, int j, int k):
    return (int)((j-i)+5+5*(i-2)-(1./2.)*(i-1)*(i-2)+15*(k-1)-1)

cdef int ind(int i, int j, int k):
    return (int)((j-i)+5+5*(i-2)-(1./2.)*(i-1)*(i-2)+15*(k-1)-1)

def object_condition(block, side_length, sphere_bound):
    # find min and max on block
    blkmin = np.array([0.0]*90)
    blkmax = np.array([0.0]*90)
    for i in range(90):
        blkmin[i] = block[i] - side_length
        blkmax[i] = block[i] + side_length

    def get_min(i, j, k):
        if i <= 6 and j <= 6 and k <= 6 and i < j:
            assert(0 <= ind(i,j,k) <= 89)
            return blkmin[ind(i, j, k)]
        return 0.0

    def get_max(i, j, k):
        if i <= 6 and j <= 6 and k <= 6 and i < j:
            assert(0 <= ind(i,j,k) <= 89)
            return blkmax[ind(i, j, k)]
        return 0.0

    # unimodular condition
    unimin = 0.0
    unimax = 0.0
    for i in range(1, 7):
        for j in range(i+1, 7):
            unimin += get_min(i, j, j)
            unimax += get_max(i, j, j)
    if not unimin <= 0. <= unimax:
        print "Failed unimodular"
        return False

    # sphere condition
    s = 0.0
    b = sphere_bound
    for i in range(90):
        s += block[i]**2
    m = math.sqrt(s)
    if not (m - b) <= 1.0 <= (m + b):
        print "Failed sphere"
        return False

    def poly_min_max(terms, i, j, k, l, m=None):
        vars = [i, j, k, l, m]

        def term(expr):
            if type(expr) is not float:
                argcnt = 0
                args = [0]*3
                for exprcnt in range(3):
                    args[argcnt] = vars[expr[exprcnt]]
                    argcnt += 1
                return get_min(args[0], args[1], args[2]), get_max(args[0], args[1], args[2])
            else:
                return expr, expr

        mins = list()
        maxes = list()
        for t in terms:
            tmin = tmax = 1.0
            for i in t:
                valmin, valmax = term(i)
                tmp1 = tmin*valmin
                tmp2 = tmin*valmax
                tmp3 = tmax*valmin
                tmp4 = tmax*valmax
                if tmp1 < tmp2:
                    tmin = tmp1
                else:
                    tmin = tmp2
                if tmp3 > tmp4:
                    tmax = tmp3
                else:
                    tmax = tmp4

            mins.append(tmin)
            maxes.append(tmax)

        return sum(mins), sum(maxes)

    # jacobi condition
    # i=0, j=1, k=2, l=3, m=4
    jacterms = (((1, 2, 4), (4, 2, 3)), ((1, 2, 4), (4, 0, 3)), ((2, 0, 4), (4, 1, 3)))

    for k in range(1, 7):
        for i in range(1, 7):
            for j in range(i+1, 7):
                jacmin = jacmax = 0.0
                for l in range(1, 7):
                    for m in range(1, 7):
                        # note that multiple neg terms can result in positive answer that mimics that of the maximum
                        #jacmin += get_min(i, j, m)*get_min(m, k, l)+get_min(j, k, m)*get_min(m, i, l) \
                        #    + get_min(k, i, m)*get_min(m, j, l)
                        #jacmax += get_max(i, j, m)*get_max(m, k, l)+get_max(j, k, m)*get_max(m, i, l) \
                        #    + get_max(k, i, m)*get_max(m, j, l)
                        rmin, rmax = poly_min_max(jacterms, i, j, k, l, m)
                        jacmin += rmin
                        jacmax += rmax
                if not jacmin <= 0. <= jacmax:
                    print "Failed Jacobi"
                    return False

    # einstein condition
    # i=0, j=1, k=2, l=3
    einterms = ((-1./2., (0, 2, 3), (1, 2, 3)), ((-1./2.), (1, 2, 3), (0, 3, 2)), ((1./4.), (2, 3, 0), (2, 3, 1)))

    def ric(i, j):
        smin = 0.0
        smax = 0.0
        for k in range(1, 7):
            for l in range(1, 7):
                #smin += - (1./2.)*get_min(i, k, l)*get_min(j, k, l) - (1./2.)*get_min(j, k, l)*get_min(i, l, k) \
                #    + (1./4.)*get_min(k, l, i)*get_min(k, l, j)
                #smax += - (1./2.)*get_max(i, k, l)*get_max(j, k, l) - (1./2.)*get_max(j, k, l)*get_max(i, l, k) \
                #    + (1./4.)*get_max(k, l, i)*get_max(k, l, j)
                rmin, rmax = poly_min_max(einterms, i, j, k, l)
                smin += rmin
                smax += rmax
        return smin, smax

    for i in range(1, 7):
        for j in range(1, 7):
            if i is not j:
                ijmin, ijmax = ric(i, j)
                iimin, iimax = ric(i, i)
                jjmin, jjmax = ric(j, j)

                if not ijmin <= 0. <= ijmax:
                    print "Failed: No Einstein metrics"
                    return False

                if not (iimin - jjmax) <= 0. <= (iimax - jjmin):
                    print "Failed: No possibility of Einstein metrics"
                    return False
    return True