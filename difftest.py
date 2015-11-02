from numpy import genfromtxt
from numpy import allclose
import numpy as np

A = genfromtxt('A.csv', delimiter=',')
A_np = genfromtxt('Anp.csv', delimiter=',')
B = genfromtxt('B.csv', delimiter=',')
B_np = genfromtxt('Bnp.csv', delimiter=',')

assert (A.shape == A_np.shape)
assert (B.shape == B_np.shape)

max_index = np.unravel_index(np.argmax(A-A_np), A.shape)
if np.max(A-A_np) < 1e-6:
    print "A matrices are the same"
else:
    print "Index of the maximum difference for A: %s" % (max_index,)
    print "MATLAB value at the maximum difference for A: %f" % A[max_index]
    print "Python value at the maximum difference for A: %f" % A_np[max_index]

max_index = np.unravel_index(np.argmax(B-B_np), B.shape)
if np.max(B-B_np) < 1e-6:
    print "B matrices are the same"
else:
    print "Index of the maximum difference for B: %s" % (max_index,)
    print "MATLAB value at the maximum difference for B: %f" % B[max_index]
    print "Python value at the maximum difference for B: %f" % B_np[max_index]
# assert (allclose(A, A_np))
# assert (allclose(B, B_np))
