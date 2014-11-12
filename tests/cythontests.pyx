__author__ = 'Lucas Schuermann'

# See notes for the derivation of the index function
# Testing implementation using different methodologies in Cython


def ind(int i, int j, int k):
    return ((j-i)+5+5*(i-2)-(1./2.)*(i-1)*(i-2)+15*(k-1))

def ind2(int i, int j, int k):
    return (int)((j-i)+5+5*(i-2)-(1./2.)*(i-1)*(i-2)+15*(k-1))
