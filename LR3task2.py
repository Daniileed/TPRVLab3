from mpi4py import MPI
import time
import random

comm = MPI.COMM_WORLD

size = 1024

Am = [0]*size
Bm = [0]*size
M = [0]*size

for i in range(size):
    Am[i] = [0]*size
    Bm[i]= [0]*size
    M[i]= [0]*size


for i in range(size):
    for j in range(size):
        Am[i][j] = random.randint(0,6)
        Bm[i][j] = random.randint(0,6)

def CalculateMatrix(start, end):
    for i in range(start, end):
        for j in range(size):
            for k in range(size):
                M[i][j] += Am[i][k]*Bm[k][j]
    print(f"Process {comm.Get_rank()} completed calculation.")


start = time.time()
MPI.Init
if (comm.Get_rank() == 0):
    CalculateMatrix(0, size//comm.Get_size())

elif (comm.Get_rank() == 1):
    CalculateMatrix((size//comm.Get_size()) + 1, size//comm.Get_size()*2)

elif (comm.Get_rank() == 2):
    CalculateMatrix((size//comm.Get_size()*2)+1, size//comm.Get_size()*2)
    
elif (comm.Get_rank() == 3):
    CalculateMatrix((size//comm.Get_size()*3)+1, size)


MPI.Finalize()
end = time.time()

print(f"Time: {(end-start)*1000} milliseconds")