#Rosalind.info/problems/

#20200716
"""
#1. counting DNA nucleotides, .count

seq=input("input DNA sequence")
print(seq.count('A'),seq.count('C'),seq.count('G'),seq.count('T'))

#2.Transcribing DNA into RNA .replace

seq=input("input DNA sequence")
print("RNA sequence : ",seq.replace("T","U"))

#3. Complementing a Strand of DNA

seq=input("input DNA sequence")
seq=seq.replace("A","t").replace("T","a").replace("G","c").replace("C","g")
seq=seq.upper()
seq=seq[::-1]
print("complementing sequence :", seq)

"""
#4. Rabbits and Recurrence Relations
# n month 뒤의 rabbit pairs k 씩 낳는다, 애기를 낳기 위한 성체 토끼가 되기 위해 한달의 시간이 필요하다.

n=int(input("how long(month): "))
k=int(input("how many(pairs): "))

def FIB(n,k):
    fib=[]
    for i in range(n):
        if i< 2:
            fib.append(1)
        else:
            fib.append(fib[i-1]+(k*fib[i-2]))
    return fib
result=FIB(n,k)
print(result)

#다른 방식의 풀이
import sys

def fib(n:int) -> int:
    if n==0:
        return 0
    elif n==1:
        return 1
    else:
        return fib(n-1) + fib(n-2) #함수를 return 가능

n=int(sys.argv[1])

print(fib(n))
















