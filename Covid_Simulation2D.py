
# Author: Shambhavi Nandan


import matplotlib.pyplot as plt
#get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
import numpy as np
#from scipy import linalg


def exchange_rows(a):
    r, c = a.shape
    a1 = np.zeros((r, c))
    for i in range(0, r):
        a1[i] = a[-i -1]
    
    return a1


def solve_Succeptibility(Ds,Ic_old,Sc_old,dt,nx,ny):
    
    # Succeptibility datastructure:
    ac = np.zeros((ny,nx))
    al = np.zeros((ny,nx))
    ar = np.zeros((ny,nx))
    at = np.zeros((ny,nx))
    ab = np.zeros((ny,nx))
    source = np.zeros((ny,nx))
    jmin = 1
    jmax = ny-2
    for j in np.arange(jmin, jmax+1):
        if j==jmin: # top row
            imin = 1
            imax = nx-2
            for i in np.arange(imin, imax+1):
                if i==1: # left corner node:
                    ac[j,i] = (1./dt) + Ic_old[j,i] + 4*Ds/dx**2
                    al[j,i] = 0.
                    ar[j,i] = Ds/dx**2
                    at[j,i] = 0.
                    ab[j,i] = Ds/dx**2
                    source[i,j] = Sc_old[j,i]/dt
                elif i>imin and i<imax: # boundary nodes:
                    ac[j,i] = (1./dt) + Ic_old[j,i] + 4*Ds/dx**2
                    al[j,i] = Ds/dx**2
                    ar[j,i] = Ds/dx**2
                    at[j,i] = 0.
                    ab[j,i] = Ds/dx**2
                    source[j,i] = Sc_old[j,i]/dt
                elif i==imax: # right corner node:
                    ac[j,i] = (1./dt) + Ic_old[j,i] + 4*Ds/dx**2
                    al[j,i] = Ds/dx**2
                    ar[j,i] = 0.
                    at[j,i] = 0.
                    ab[j,i] = Ds/dx**2
                    source[j,i] = Sc_old[j,i]/dt

        elif j==jmax: # bottom row
            imin = 1
            imax = nx-2
            for i in np.arange(imin, imax+1):
                if i==imin: # left corner node:
                    ac[j,i] = (1./dt) + Ic_old[j,i] + 4*Ds/dx**2
                    al[j,i] = 0.
                    ar[j,i] = Ds/dx**2
                    at[j,i] = Ds/dx**2
                    ab[j,i] = 0.
                    source[j,i] = Sc_old[j,i]/dt
                elif i>imin and i<imax: # boundary nodes:
                    ac[j,i] = (1./dt) + Ic_old[j,i] + 4*Ds/dx**2
                    al[j,i] = Ds/dx**2
                    ar[j,i] = Ds/dx**2
                    at[j,i] = Ds/dx**2
                    ab[j,i] = 0.
                    source[j,i] = Sc_old[j,i]/dt
                elif i==imax: # right corner node:
                    ac[j,i] = (1./dt) + Ic_old[j,i] + 4*Ds/dx**2
                    al[j,i] = Ds/dx**2
                    ar[j,i] = 0.
                    at[j,i] = Ds/dx**2
                    ab[j,i] = 0.
                    source[j,i] = Sc_old[j,i]/dt

        else: # internal rows
            imin = 1
            imax = nx-2
            for i in np.arange(imin, imax+1):
                if i==imin: # left boundary node:
                    ac[j,i] = (1./dt) + Ic_old[j,i] + 4*Ds/dx**2
                    al[j,i] = 0.
                    ar[j,i] = Ds/dx**2
                    at[j,i] = Ds/dx**2
                    ab[j,i] = Ds/dx**2
                    source[j,i] = Sc_old[j,i]/dt
                elif i>imin and i<imax: # internal nodes:
                    ac[j,i] = (1./dt) + Ic_old[j,i] + 4*Ds/dx**2
                    al[j,i] = Ds/dx**2
                    ar[j,i] = Ds/dx**2
                    at[j,i] = Ds/dx**2
                    ab[j,i] = Ds/dx**2
                    source[j,i] = Sc_old[j,i]/dt
                elif i==imax: # right boundary node:
                    ac[j,i] = (1./dt) + Ic_old[j,i] + 4*Ds/dx**2
                    al[j,i] = Ds/dx**2
                    ar[j,i] = 0.
                    at[j,i] = Ds/dx**2
                    ab[j,i] = Ds/dx**2
                    source[j,i] = Sc_old[j,i]/dt
    
    A = assemble_a_to_A(ny-2, nx-2, ac[1:-1,1:-1],ar[1:-1,1:-1],al[1:-1,1:-1],at[1:-1,1:-1],                        ab[1:-1,1:-1])
    sol = np.linalg.solve(A,source[1:-1,1:-1].flatten())
    
    return sol

def solve_Infection(Di,Ic_old,Sc_old,dt,nx,ny):
    
    # Infection datastructure:
    ac = np.zeros((ny,nx))
    al = np.zeros((ny,nx))
    ar = np.zeros((ny,nx))
    at = np.zeros((ny,nx))
    ab = np.zeros((ny,nx))
    source = np.zeros((ny,nx))
    jmin = 1
    jmax = ny-2
    for j in np.arange(jmin, jmax+1):
        if j==jmin: # top row
            imin = 1
            imax = nx-2
            for i in np.arange(imin, imax+1):
                if i==1: # left corner node:
                    ac[j,i] = (1./dt) + 0. + 4*Ds/dx**2
                    al[j,i] = 0.
                    ar[j,i] = Ds/dx**2
                    at[j,i] = 0.
                    ab[j,i] = Ds/dx**2
                    source[i,j] = Ic_old[j,i]*Sc_old[j,i] + Ic_old[j,i]/dt
                elif i>imin and i<imax: # boundary nodes:
                    ac[j,i] = (1./dt) + 0. + 4*Ds/dx**2
                    al[j,i] = Ds/dx**2
                    ar[j,i] = Ds/dx**2
                    at[j,i] = 0.
                    ab[j,i] = Ds/dx**2
                    source[j,i] = Ic_old[j,i]*Sc_old[j,i] + Ic_old[j,i]/dt
                elif i==imax: # right corner node:
                    ac[j,i] = (1./dt) + 0. + 4*Ds/dx**2
                    al[j,i] = Ds/dx**2
                    ar[j,i] = 0.
                    at[j,i] = 0.
                    ab[j,i] = Ds/dx**2
                    source[j,i] = Ic_old[j,i]*Sc_old[j,i] + Ic_old[j,i]/dt

        elif j==jmax: # bottom row
            imin = 1
            imax = nx-2
            for i in np.arange(imin, imax+1):
                if i==imin: # left corner node:
                    ac[j,i] = (1./dt) + 0. + 4*Ds/dx**2
                    al[j,i] = 0.
                    ar[j,i] = Ds/dx**2
                    at[j,i] = Ds/dx**2
                    ab[j,i] = 0.
                    source[j,i] = Ic_old[j,i]*Sc_old[j,i] + Ic_old[j,i]/dt
                elif i>imin and i<imax: # boundary nodes:
                    ac[j,i] = (1./dt) + 0. + 4*Ds/dx**2
                    al[j,i] = Ds/dx**2
                    ar[j,i] = Ds/dx**2
                    at[j,i] = Ds/dx**2
                    ab[j,i] = 0.
                    source[j,i] = Ic_old[j,i]*Sc_old[j,i] + Ic_old[j,i]/dt
                elif i==imax: # right corner node:
                    ac[j,i] = (1./dt) + 0. + 4*Ds/dx**2
                    al[j,i] = Ds/dx**2
                    ar[j,i] = 0.
                    at[j,i] = Ds/dx**2
                    ab[j,i] = 0.
                    source[j,i] = Ic_old[j,i]*Sc_old[j,i] + Ic_old[j,i]/dt

        else: # internal rows
            imin = 1
            imax = nx-2
            for i in np.arange(imin, imax+1):
                if i==imin: # left boundary node:
                    ac[j,i] = (1./dt) + 0. + 4*Ds/dx**2
                    al[j,i] = 0.
                    ar[j,i] = Ds/dx**2
                    at[j,i] = Ds/dx**2
                    ab[j,i] = Ds/dx**2
                    source[j,i] = Ic_old[j,i]*Sc_old[j,i] + Ic_old[j,i]/dt
                elif i>imin and i<imax: # internal nodes:
                    ac[j,i] = (1./dt) + 0. + 4*Ds/dx**2
                    al[j,i] = Ds/dx**2
                    ar[j,i] = Ds/dx**2
                    at[j,i] = Ds/dx**2
                    ab[j,i] = Ds/dx**2
                    source[j,i] = Ic_old[j,i]*Sc_old[j,i] + Ic_old[j,i]/dt 
                elif i==imax: # right boundary node:
                    ac[j,i] = (1./dt) + 0. + 4*Ds/dx**2
                    al[j,i] = Ds/dx**2
                    ar[j,i] = 0.
                    at[j,i] = Ds/dx**2
                    ab[j,i] = Ds/dx**2
                    source[j,i] = Ic_old[j,i]*Sc_old[j,i] + Ic_old[j,i]/dt
    
    A = assemble_a_to_A(ny-2, nx-2, ac[1:-1,1:-1],ar[1:-1,1:-1],al[1:-1,1:-1],at[1:-1,1:-1],                        ab[1:-1,1:-1])
    sol = np.linalg.solve(A,source[1:-1,1:-1].flatten())
    
    return sol

def solve_Recovery(Ic_old,Rc_old,dt,nx,ny):
    
    # Infection datastructure:
    ac = np.zeros((ny,nx))
    al = np.zeros((ny,nx))
    ar = np.zeros((ny,nx))
    at = np.zeros((ny,nx))
    ab = np.zeros((ny,nx))
    source = np.zeros((ny,nx))
    jmin = 1
    jmax = ny-2
    for j in np.arange(jmin, jmax+1):
        if j==jmin: # top row
            imin = 1
            imax = nx-2
            for i in np.arange(imin, imax+1):
                if i==1: # left corner node:
                    ac[j,i] = 1./dt
                    al[j,i] = 0.
                    ar[j,i] = 0.
                    at[j,i] = 0.
                    ab[j,i] = 0.
                    source[i,j] = Ic_old[j,i] + Rc_old[j,i]/dt
                elif i>imin and i<imax: # boundary nodes:
                    ac[j,i] = 1./dt
                    al[j,i] = 0.
                    ar[j,i] = 0.
                    at[j,i] = 0.
                    ab[j,i] = 0.
                    source[i,j] = Ic_old[j,i] + Rc_old[j,i]/dt
                elif i==imax: # right corner node:
                    ac[j,i] = 1./dt
                    al[j,i] = 0.
                    ar[j,i] = 0.
                    at[j,i] = 0.
                    ab[j,i] = 0.
                    source[i,j] = Ic_old[j,i] + Rc_old[j,i]/dt

        elif j==jmax: # bottom row
            imin = 1
            imax = nx-2
            for i in np.arange(imin, imax+1):
                if i==imin: # left corner node:
                    ac[j,i] = 1./dt
                    al[j,i] = 0.
                    ar[j,i] = 0.
                    at[j,i] = 0.
                    ab[j,i] = 0.
                    source[i,j] = Ic_old[j,i] + Rc_old[j,i]/dt
                elif i>imin and i<imax: # boundary nodes:
                    ac[j,i] = 1./dt
                    al[j,i] = 0.
                    ar[j,i] = 0.
                    at[j,i] = 0.
                    ab[j,i] = 0.
                    source[i,j] = Ic_old[j,i] + Rc_old[j,i]/dt
                elif i==imax: # right corner node:
                    ac[j,i] = 1./dt
                    al[j,i] = 0.
                    ar[j,i] = 0.
                    at[j,i] = 0.
                    ab[j,i] = 0.
                    source[i,j] = Ic_old[j,i] + Rc_old[j,i]/dt

        else: # internal rows
            imin = 1
            imax = nx-2
            for i in np.arange(imin, imax+1):
                if i==imin: # left boundary node:
                    ac[j,i] = 1./dt
                    al[j,i] = 0.
                    ar[j,i] = 0.
                    at[j,i] = 0.
                    ab[j,i] = 0.
                    source[i,j] = Ic_old[j,i] + Rc_old[j,i]/dt
                elif i>imin and i<imax: # internal nodes:
                    ac[j,i] = 1./dt
                    al[j,i] = 0.
                    ar[j,i] = 0.
                    at[j,i] = 0.
                    ab[j,i] = 0.
                    source[i,j] = Ic_old[j,i] + Rc_old[j,i]/dt
                elif i==imax: # right boundary node:
                    ac[j,i] = 1./dt
                    al[j,i] = 0.
                    ar[j,i] = 0.
                    at[j,i] = 0.
                    ab[j,i] = 0.
                    source[i,j] = Ic_old[j,i] + Rc_old[j,i]/dt
    
    A = assemble_a_to_A(ny-2, nx-2, ac[1:-1,1:-1],ar[1:-1,1:-1],al[1:-1,1:-1],at[1:-1,1:-1],                        ab[1:-1,1:-1])
    sol = np.linalg.solve(A,source[1:-1,1:-1].flatten())
    
    return sol

def i_j_to_k(index, columns):
    return index[0] * columns + index[1]

def R(index):
    i, j = index
    return (i, j + 1)

def L(index):
    i, j = index
    return (i, j - 1)

def T(index):
    i, j = index
    return (i - 1, j)

def B(index):
    i, j = index
    return (i + 1, j)

def assemble_a_to_A(rows, columns, aPs, aEs, aWs, aNs, aSs):
    
    A = np.zeros((rows * columns, rows *  columns))
    
    row = 0
    for index in np.ndindex(rows, columns):
        
        y = np.zeros(rows * columns)
        
        k = i_j_to_k(index, columns)
        y[k] = aPs[index]
        
        if index == (0, 0): # top left corner cell
            E_index = R(index)
            k = i_j_to_k(E_index, columns)
            y[k] = -aEs[index]
            
            S_index = B(index)
            k = i_j_to_k(S_index, columns)
            y[k] = -aSs[index]
        
        elif index == (rows - 1, 0): # bottom left corner cell
            E_index = R(index)
            k = i_j_to_k(E_index, columns)
            y[k] = -aEs[index]
            
            N_index = T(index)
            k = i_j_to_k(N_index, columns)
            y[k] = -aNs[index]
            
        elif index == (0, columns - 1): # top right corner cell
            W_index = L(index)
            k = i_j_to_k(W_index, columns)
            y[k] = -aWs[index]
            
            S_index = B(index)
            k = i_j_to_k(S_index, columns)
            y[k] = -aSs[index]
            
        elif index == (rows - 1, columns - 1): # bottom right corner cell
            W_index = L(index)
            k = i_j_to_k(W_index, columns)
            y[k] = -aWs[index]
            
            N_index = T(index)
            k = i_j_to_k(N_index, columns)
            y[k] = -aNs[index]
            
        elif index[1] == 0: # column 0 cells excluding top left and bottom left corner
            E_index = R(index)
            k = i_j_to_k(E_index, columns)
            y[k] = -aEs[index]
            
            N_index = T(index)
            k = i_j_to_k(N_index, columns)
            y[k] = -aNs[index]
            
            S_index = B(index)
            k = i_j_to_k(S_index, columns)
            y[k] = -aSs[index]
            
        elif index[0] == 0: # row 0 cells excluding top left and top right corner
            W_index = L(index)
            k = i_j_to_k(W_index, columns)
            y[k] = -aWs[index]
            
            E_index = R(index)
            k = i_j_to_k(E_index, columns)
            y[k] = -aEs[index]
            
            S_index = B(index)
            k = i_j_to_k(S_index, columns)
            y[k] = -aSs[index]
            
        elif index[1] == columns - 1: # column columns - 1 cells excluding top and bottom corner
            W_index = L(index)
            k = i_j_to_k(W_index, columns)
            y[k] = -aWs[index]
            
            N_index = T(index)
            k = i_j_to_k(N_index, columns)
            y[k] = -aNs[index]
            
            S_index = B(index)
            k = i_j_to_k(S_index, columns)
            y[k] = -aSs[index]
            
        elif index[0] == rows - 1: # row rows - 1 cells excluding top and bottom corner
            W_index = L(index)
            k = i_j_to_k(W_index, columns)
            y[k] = -aWs[index]
            
            E_index = R(index)
            k = i_j_to_k(E_index, columns)
            y[k] = -aEs[index]
            
            N_index = T(index)
            k = i_j_to_k(N_index, columns)
            y[k] = -aNs[index]
            
        else: # all interior cells
            W_index = L(index)
            k = i_j_to_k(W_index, columns)
            y[k] = -aWs[index]
            
            E_index = R(index)
            k = i_j_to_k(E_index, columns)
            y[k] = -aEs[index]
            
            N_index = T(index)
            k = i_j_to_k(N_index, columns)
            y[k] = -aNs[index]
            
            S_index = B(index)
            k = i_j_to_k(S_index, columns)
            y[k] = -aSs[index]
        
        A[row, :] = y[:] 
        
        row += 1
    
    return A

# Grid parameters:
nx = 40
ny = nx
lx = 100
ly = lx

# Time parameters:
nt = 150.

dx = lx / nx
dy = ly / ny


# Succeptibility random initialization:
S = np.ones((ny, nx))
S[1,1] = 5.
S[2,3] = 6.
S[3,4] = 5.
S[2,4] = 6.
#S[18:20,20] = 1.0
#S[1:-1,1:-1] = np.random.uniform(low=0.0, high=1.0, size=(ny-2,nx-2))
# Infection initialization:
I = np.zeros((ny, nx))
I[3,4] = 1.
#I[1:-1,1:-1] = np.random.uniform(low=0.0, high=0.1, size=(ny-2,nx-2))
#I[1:-1,1:-1] = np.random.uniform(low=0.5, high=1.0, size=(ny-2,nx-2))
# Recovery initialization:
Rc = np.zeros((ny, nx))
Rc[1:-1,1:-1] = 0.0

# Parameters:
Ds = 1.0e-1
Di = 1.0e-1
dt = 1.0e-1

S_old = np.zeros((ny, nx))
I_old = np.zeros((ny, nx))
R_old = np.zeros((ny, nx))

t = 0.
while t < nt:
    S_old[1:-1,1:-1] = S[1:-1,1:-1]
    I_old[1:-1,1:-1] = I[1:-1,1:-1]
    R_old[1:-1,1:-1] = Rc[1:-1,1:-1]
    I_sol = solve_Infection(Di,I_old,S_old,dt,nx,ny)
    S_sol = solve_Succeptibility(Ds,I_old,S_old,dt,nx,ny)
    #R_sol = solve_Recovery(I_old,R_old,dt,nx,ny)
    S[1:-1,1:-1] = np.reshape(S_sol,(ny-2,nx-2))
    I[1:-1,1:-1] = np.reshape(I_sol,(ny-2,nx-2))
    #Rc[1:-1,1:-1] = np.reshape(R_sol,(ny-2,nx-2))

    t = t+dt


X = np.linspace(0., lx, nx)
Y = np.linspace(0., ly, ny)
# plotting contours
#plt.figure(1)
#e = plt.contourf(Y, X, Rc, cmap='RdBu')
#plt.colorbar(e)
#plt.figure(2)
#e = plt.contourf(Y, X, S, cmap='ocean_r')
#plt.colorbar(e)
plt.figure()
e = plt.contourf(Y, X, I, cmap='RdBu')
plt.colorbar(e)
plt.show()


