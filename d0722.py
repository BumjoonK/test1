
class C:
    def __init__ (self):
        print("Class C의 인스턴스가 생성됨")
        self.name = "ccc"
        self.age = 0

    def say_hi (self):
        print("hi")

    def add_age(self, n:int):
        self.age +=n

#    def __str__ (self):
#        retrun "__str__   called"
#    def __repr__ (self):
#        retrun "__repr__ called"
#    def __abs__ (self):
#        print ("__abs__ 호출됨")
#    def __len__ (self):
#        print( "__len__ 호출됨")
#    def __add__ (self, other):
#        return self.age + other.age


#바이오 파이썬 이용해서 fasta
from Bio import SeqIO

record =SeqIO.read("059.fasta", "fasta")

A=record.seq.count("A")
C=record.seq.count("C")
G=record.seq.count("G")
T=record.seq.count("T")

print(f"A: {A}") # A:497
print(f"C: {C}") # C:444
print(f"G: {G}") # G:585
print(f"T: {T}") # T:514


#k-mer generation

import sys

def mer(l1, l2, n):
    if n==1:
        return l2
    ltmp=[]       
    for s1 in l1:
        for s2 in l2:
            ltmp.append(s1+s2)

    return mer(l1,ltmp,n-1)

l1=["A","C","G","T"]
l2=["A","C","G","T"]
n=int(sys.argv[1])

print(mer(l1,l2,n)
