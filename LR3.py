from mpi4py import MPI
import hashlib
import time

P_alphavit = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
empty_passward = ''
empty_hash = ''
hash = hashlib.md5()
comm = MPI.COMM_WORLD

passward = b'0Wj'

hash.update(passward)
empty_hash = hash.hexdigest()
def bruteForeceSIngle (begin, end):
    for i in range(begin, end):
        for j in range(len(P_alphavit)):
            for k in range(len(P_alphavit)):
                hash = hashlib.md5()
                empty_passward = f"{P_alphavit[i]}{P_alphavit[j]}{P_alphavit[k]}"
                empty_passward = bytes(empty_passward, "utf-8")
                hash.update(empty_passward)
                passward = hash.hexdigest()
                if (empty_hash == passward):
                    print("Password FOUND!", f"{P_alphavit[i]}{P_alphavit[j]}{P_alphavit[k]}")

def bruteForece (begin, end):
    for i in range(begin, end):
        for j in range(len(P_alphavit)):
            for k in range(len(P_alphavit)):
                hash = hashlib.md5()
                empty_passward = f"{P_alphavit[i]}{P_alphavit[j]}{P_alphavit[k]}"
                empty_passward = bytes(empty_passward, "utf-8")
                hash.update(empty_passward)
                passward = hash.hexdigest()
                if (empty_hash == passward):
                    print("Password FOUND!", f"{P_alphavit[i]}{P_alphavit[j]}{P_alphavit[k]} by proccess {comm.Get_rank()+1}")

                    

MPI.Init  

if (comm.Get_rank() == 0):
    start_1 = time.time()
    bruteForeceSIngle(0, 62)
    end_1 = time.time()
    print(f"Single-prcess Time: {(end_1-start_1)*1000} milliseconds")

start_2 = time.time()

if (comm.Get_rank() == 0):
    bruteForece (0, 16)
elif (comm.Get_rank() == 1):
    bruteForece (17, 32)
elif (comm.Get_rank() == 2):
    bruteForece (33, 48)
elif (comm.Get_rank() == 3):
    bruteForece (49, 62)

end_2 = time.time()

print(f"Multi-prcess Time: {(end_2-start_2)*1000} milliseconds Process {comm.Get_rank()+1}")
MPI.Finalize()









