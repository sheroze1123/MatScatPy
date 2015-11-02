import matplotlib.pyplot as plt
import numpy as np
def chebdifft(f,M,Nout):
    #need to add a check if f is a numpy array
    N = len(f)
    c= np.zeros(N)
    c[0] = 0.5/(N-1)
    c[N-1] = 0.5/(N-1)
    for j in range(1,N-1):
        c[j] = 1/(N-1)
    a0 = np.fft.fft(np.concatenate([f,f[N-2:0:-1]]))
    a0[0:N] = a0[0:N]*c
    a = np.zeros((N,M+1))
    a[:,0] = a0[0:N]
    for ell in range(1,M+1):
        a[N-ell-1,ell] = 2*(N-ell)*a[N-ell,ell-1]
        for j in range(N-ell-2,0,-1):
            a[j,ell] = a[j+2,ell] + 2*(j+1)*a[j+1,ell-1]
        a[0,ell] = 0.5*a[2,ell] + a[1,ell-1]
        dback = np.zeros(2*(N-1))
        dback[0] = 2*a[0,M]
        dback[1:N-1] = a[1:N-1,M]
        dback[N-1] = 2*a[N-1,M]
        dback[N:] = a[N-2:0:-1,M]
        Dmf = 0.5*(np.fft.fft(dback)) #check if there are factors while doing inverse fft
        back = np.zeros(2*(N-1))
        back[0] = 2*a[0,0]
        bback[1:N-1] = a[1:N-1,0]
        back[N-1] = 2*a[N-1,0]
        back[N:] = a[N-2:0:-1,0]
        f2 = 0.5*(np.fft.fft(back)) #check if there are factors while doing inverse fft
        
    if np.amax(np.absolute(f.imag)) == 0:
        return (Dmf[0:Nout].real,f2[0:Nout].real)
        
    else:
        return (Dmf[0:Nout],f2[0:Nout])
