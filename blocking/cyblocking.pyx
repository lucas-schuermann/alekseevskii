__author__ = 'Lucas Schuermann'

cdef:
    struct pyb:
        int ind(int i, int j, int k):
            return (int)((j-i)+5+5*(i-2)-(1./2.)*(i-1)*(i-2)+15*(k-1)-1)
