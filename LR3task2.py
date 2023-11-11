from mpi4py import MPI
import time
import random


comm = MPI.COMM_WORLD
ProcessNumber = comm.Get_size()
rank = comm.Get_rank()
size = 4

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

def PrintMatrix():
    for i in range(size):
        for j in range(size):
            print(Am[i][j]," ",Bm[i][j], " ", M[i][j], MP[i][j], end = '')
            print()

def CompareMatrixes():
    C = True
    for i in range(size):
     for j in range(size):
         if M[i][j]!=MP[i][j]:
             C = False
    return "Matrix is equel" if C == True else "Matrix not equel"

def RecieveResult(begin , end, source):
    for i in range(begin, end):
        for j in range(size):
         MP[i][j] = comm.recv(source = source)

def SendResult(start, end):
    for i in range(start, end):
        for j in range(size):
            comm.send(MP[i][j],dest = 0)

def RecieveMatrixes(start,end):
    for i in range(start, end):
        for j in range(size):
            Am[i][j] = comm.recv(source = 0)
            Bm[i][j] = comm.recv(source = 0)


MPI.Init



if (rank == 0):
    for i in range(size):
         for j in range(size):
            Am[i][j] = int(random.uniform(0,6))
            Bm[i][j] = int(random.uniform(0,6))
           
            

for i in range(size):
    for j in range(size):
        Am[i][j] = comm.bcast(Am[i][j], root = 0)
        Bm[i][j] = comm.bcast(Bm[i][j], root = 0)  
    

if (rank == 0):
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
    PrintMatrix()

if (rank == 1):
    CalculateMatrix((size//ProcessNumber) + 1, size//ProcessNumber*2)
    SendResult((size//ProcessNumber) + 1, size//ProcessNumber*2)
    PrintMatrix()

    

if (rank == 2):
    CalculateMatrix(((size//ProcessNumber)*2)+1, size//ProcessNumber*3)
    SendResult(((size//ProcessNumber)*2)+1, size//ProcessNumber*3)
    PrintMatrix()
    

if (rank == 3):
    CalculateMatrix((size//ProcessNumber*3)+1, size)
    SendResult((size//ProcessNumber*3)+1, size)
    PrintMatrix()
    
    
end_2 = time.time()


print(f"Time multi-process: {(end_2-start_2)*1000} milliseconds")

MPI.Finalize()