import numpy as np
def cubic_spline_get_coeffs(X,Y,clamped=False, dx0=0.0, dxn=0.0):
    """
    Object: Compute the spline coefficients for a
        natural or clamped cubic spline interpolant.
        Adapted from Mathews & Fink 4th ed, Program 5.3
        with modifications made for free end conditions.
    Usage:
        for the natural cubic spline:
             S=cubic_spline_get_coeffs(X,Y)
        for clamped cubic spline:
             S=cubic_spline_get_coeffs(X, Y, True, dx0, dxn)
    Input:
        X: an array, the x coordinates for the knots,
             sorted in ascending order
        Y: an array, the y coordinates for the knots
             if clamped == False, it is assumed that
               free end conditions are used.
             if clamped == True, it is assumed that
                clamped end conditions are used. The
                slope at the first knot is dx0, the slope at
                the last knot is dxn. 
    Output:
        S: the rows of S are the coefficients,
             the cubic for the interval between X(k) and X(k+1) is
    S[k,0]*(x-X[k])^3 + S[k,1]*(x-X[k])^2 + S[k,2]*(x-X[k]) + S[k,3]
    """
    N=X.size-1
    LY=Y.size
    H=np.diff(np.double(X))
    D=np.diff(Y)/H
    A=H[1:N]
    B=2*(H[:N-1]+H[1:])
    C=H[1:]
    U=6*np.diff(D)
    if (clamped):
        # Clamped cubic spline endpoint conditions
        B[0]=B[0]-H[0]*0.5
        U[0]=U[0]-3.0*(D[0]-dx0)
        B[N-2]=B[N-2]-H[N-1]*0.5
        U[N-2]=U[N-2]-3.0*(dxn-D[N-1])
    #
    # Solve the tridiagonal system of equations
    # elimination phase
    for k in range(1,N-1):
        temp=A[k-1]/B[k-1]
        B[k]=B[k]-temp*C[k-1]
        U[k]=U[k]-temp*U[k-1]
    #
    M = np.zeros(N+1, dtype="float")
    #
    # Solve and back-substitute
    M[N-1]=U[N-2]/B[N-2]
    #
    k=N-3
    while k >= 0:
        M[k+1]=(U[k]-C[k]*M[k+2])/B[k]
        k -= 1
    #
    if (clamped):
        # Clamped cubic spline endpoint conditions
        M[0]=3.0*(D[0]-dx0)/H[0]-M[1]*0.5
        M[N]= 3.0*(dxn-D[N-1])/H[N-1]-M[N-1]*0.5
    #  else:
    #    # Free spline endpoint conditions
    #    M[0]=0
    #    M[N+1]=0
    #
    # The spline coefficients
    S = np.zeros((N,4), dtype="float")
    for k in range(N):
        S[k,0]=(M[k+1]-M[k])/(6*H[k])
        S[k,1]=M[k]*0.5
        S[k,2]=D[k]-H[k]*(2*M[k]+M[k+1])/6
        S[k,3]=Y[k]
    return S

def cubic_spline_evaluate (x_in,S,xx):
    """
    objective: Evaluate the cubic spline and its derivative.
    usage:  y, yp, ypp = cubic_spline_evaluate (x,S,xx)

    input:
        S contains the spline coefficients returned from
          cubic_spline_get_coefficients

        xx is the vector containing the x-coordinates of the knots
             it is assumed that these values are in ascending order
        x_in is the vector of points where the spline is to be evaluated

    output:
        y is the vector of y-values that go with the x-values
        yprime is the vector of first derivative values
        yprimeprime is the vector of second derivative values
    """
    if isinstance(x_in, np.ndarray):
        x = x_in
        isvector = True
    else:
        x = np.array([x_in])
        isvector = False
    m=x.size
    n=xx.size
    y=np.zeros(m, dtype="float")
    yprime=np.zeros(m, dtype="float")
    yprimeprime=np.zeros(m,dtype="float")
    for j in range(m):
        # lookup x(j)
        # find integer k such that xx(k) <= x(j) <= xx(k+1)
        if (x[j] < xx[1]):
            # first interval
            k=0
            u=1
        elif (x[j] > xx[n-2]):
            # last interval
            k=n-2
            u=n-1
        else:
            # start bisection search algorithm
            k=1
            u=n-1
            while ((u-k) > 1):
                mp=int((u+k)/2)
                if( x[j] > xx[mp]):
                    k=mp
                else:
                    u=mp
        # evaluate the cubic in nested form
        w=x[j]-xx[k]
        y[j] = ((S[k,0]*w + S[k,1])*w+S[k,2])*w+S[k,3]
        yprime[j] = (3*S[k,0]*w + 2*S[k,1])*w+S[k,2]
        yprimeprime[j] = 6*S[k,0]*w + 2*S[k,1]
    if isvector:
        return y,yprime,yprimeprime
    else:
        return y[0],yprime[0],yprimeprime[0]
