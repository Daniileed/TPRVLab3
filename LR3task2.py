from mpi4py import MPI
import time
import random


comm = MPI.COMM_WORLD
ProcessNumber = comm.Get_size()
rank = comm.Get_rank()

size = 128

Am = [0]*size
Bm = [0]*size
M = [0]*size
MP = [0]*size

for i in range(size):
    Am[i] = [0]*size
    Bm[i]= [0]*size
    M[i]= [0]*size
    MP[i] = [0]*size

def CalculateMatrix(start, end):
    for i in range(start, end):
        for j in range(size):
            for k in range(size):
                MP[i][j] += Am[i][k]*Bm[k][j]
    print(f"Process {rank} completed calculation.")

def CompareMatrixes():
    C = True
    for i in range(size):
     for j in range(size):
         if M[i][j]!=MP[i][j]:
             C = False
    return "Matrix is equel" if C == True else "Matrix not equel"

def RecieveMatrix(source):
    for i in range((source*size)//ProcessNumber + 1, ((source + 1)*size)*ProcessNumber):
        for j in range(size):
         MP[i][j] = comm.recv(source = source)

MPI.Init

if (rank == 0):
    for i in range(size):
     for j in range(size):
        Am[i][j] = random.randint(0,6)
        Bm[i][j] = random.randint(0,6)
        comm.send(Am[i][j], 1)
        comm.send(Am[i][j], 2)
        comm.send(Am[i][j], 3)

        comm.send(Bm[i][j], 1)
        comm.send(Bm[i][j], 2)
        comm.send(Bm[i][j], 3)

    start_1 = time.time()
    for i in range(size):
        for j in range(size):
            for k in range(size):
                M[i][j] += Am[i][k]*Bm[k][j]
    end_1 = time.time()
    print(f"Time single: {(end_1-start_1)*1000} milliseconds")

start_2 = time.time()
if (rank == 0):
    CalculateMatrix(0, size//ProcessNumber)
    
elif (rank == 1):
    CalculateMatrix((size//ProcessNumber) + 1, size//ProcessNumber*2)

elif (rank == 2):
    CalculateMatrix((size//ProcessNumber*2)+1, size//ProcessNumber*3)
    
elif (rank == 3):
    CalculateMatrix((size//ProcessNumber*3)+1, size)
    

end_2 = time.time()

print(CompareMatrixes())
print(f"Time multi-process: {(end_2-start_2)*1000} milliseconds")

MPI.Finalize()