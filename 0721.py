
"""
#압축된 파일 받아서 염기서열 개수 파악하기

import sys
import gzip

if len(sys.argv) !=2:
    print(f"#usage: python {sys.argv[0]} [fasta.gz]")
    sys.exit()

f=sys.argv[1]
d={}
with gzip.open(f,'rb') as handle: #b=binary
    for line in handle:
        line = line.decode("utf-8").strip() #string type으로 바꿔줌
        if line.startswith(">"):
            continue
        for s in line:
            if s in d:
                d[s] += 1
            else:
                d[s] = 1
with open("result1.txt", "w") as handle:
     handle.write(f"A: {d['A']}\n")
     handle.write(f"T: {d['T']}\n")
     handle.write(f"G: {d['G']}\n")
     handle.write(f"C: {d['C']}\n")

#문자열 변수 3칸식 건너뛰며 출력

Seq1 ="ATGTTATAG"

for i in range(0,len(Seq1),3):
    #print(i) #0,3,6
    print(i,Seq1[i]) #인덱싱
    print(i,i+3, Seq1[i:i+3]) #슬라이싱

#문자열 순서 뒤집기
print("input sequence:", Seq1)
print("Complementary sequence=", Seq1[::-1])

#문자열 바꾸기

import sys

def comp1(seq: str) ->str:
    comp=""
    for s in seq:
        if s=="A":
            comp +="T"
        elif s=="C":
            comp +="G"
        elif s=="G":
            comp +="C"
        elif s=="T":
            comp +="A"
    return comp

def comp2(seq):
    d_comp={"A":"T","T":"A","C":"G","G":"C"}
    comp=""
    for s in seq:
        comp += d_comp[s]
    return comp


if __name__ == "__main__":  #다른 파이썬에 있는 변수나 함수를 가져와서 사용
    #print(p028.comp1("ATG") Ipython에서, import 했을 때는 함수 입력 안하면 실행 안됨
    if len(sys.argv) != 2:
        print(f"#usage: python {sys.argv[0]} [string]")
        sys.exit()

    seq=sys.argv[1] #ATGTTATAG
    c1=comp1(seq)
    c2=comp2(seq)
    print(seq)
    print(c1)
    print(c2)
"""
#리스트의 요소값을 사전으로 세기
l=[3,1,1,2,0,0,2,3,3]
d={}
for i in l:
    if i in d:
        d[i]+=1
    else:
        d[i]=1
print(d)
