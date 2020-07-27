#! /usr/bin/env python
# -*- coding: utf-8 -*-

#프로그래밍 과제

#Q1.지금까지 프로그래밍 한 스크립트를 github reporsitory에 올려보세요. 디렉터리를 만들어 업로드 해도 좋고 그냥 올려도 좋고 자유입니다.

#Answer1
# 0) git status 로 상태 확인
# 1) git add . 로 모든 파일 추가
# 2) git commit -m :"메세지"로 파일 commit
# 3) git push origin master

# git pull server(인터넷) 상에서 수정한 내용을 update

#Q2 자신의 이름을 출력하는 프로그램을 작성해보세요

#Answer2
print("***Q2 문제***")
print("자신의 이름 출력, my name is Bumjoon Kim")

#Q3 염기 한글자를 받는 함수를 만들어 출력
import sys
def base(nt):
    if nt == "A":
        print("Adenine")
    elif nt == "C":
        print("Cytosine")
    elif nt == "G":
        print("Guanine")
    elif nt == "T":
        print("Thymine")
    elif nt == "U":
        print("Uracil")
    else:
        print("정확한 값을 입력해주세요")
print("***Q3 문제***")
base(sys.argv[1])

#Q4 어떠한 수 n을 입력받아 10 /n의 결과를 출력하는 프로그램을 작성해 보세요 만약에 n이 0인 경우는 어떻게 되나요? 발생하는 오류를 "try-except"로 잡아보세요.

print("***Q4 문제***")
try:
    n=int(input("Enter: "))
    print(10/n)
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다")
except ValueError:
    print("값을 입력해주세요")

#Q5 재귀 알고리즘을 사용하여 5!을 구하는 프로그램을 만들어보세요
#함수값 자체를 받아서 함수값을 다시 함수에 입력하는 방법
n=int(input("Q5, 재귀 알고리즘, 팩토리얼 n 값 입력"))

def fac(n):
    for n in range(1,n+1):
        n=n*(n+1)
    print(n)
print("***Q5 문제***")
fac(n)

#Q4 csv 파일을 json으로 바꿔보세요

print("***Q4***")
import json
import sys
def read_csv(file_name:str)->list:
    ret=[]
    with open(file_name,'r') as handle:
        for line in handle:
            if line.startswith("#"):
                header=line.strip().split(",")
                continue
            splitted=line.strip().split(",")
            d=dict(zip(header, splitted))
            ret.append(d)
    return ret
def to_json(ret):
    with open(ret"r") as handle:
        json.dump(ret, handle, indent=4)
    ret=sys.argv[1]
    ret=to_json(ret)
    print(ret)

#Q5 k-mer를 만드는 프로그램을 작성해보세요
l1=["A","C","G","T"]
l2=["A","C","G","T"]

def mer(l1,l2,n):
    if n==1:
        return 12
    ltmp=[]
    for s1 in l1:
        for s2 in l2:
            ltmp.append(s1+s2)
    return mer(l1,ltmp,n-1)

print("***Q5***")
#Q6 앞서 만든 kmer를 활용하여 7mer 중 문자열이 회문구조랴르 만족하는 문자열의 개수를 출력해보세요
print("***Q6***")
#프로그래밍 과제3
#Q1 059.fasta 파일의 각 염기를 파이썬 dictionary를 사용하여 세어보세요.

print("***Q1***")
#Q2 059.fasta 파일의 각 염기를 파이썬 dictionary를 사용하여 센 다음 결과를 j    son으로 저장
      
print("***Q2***")
       
#Q3 059 파일의 역상보서열을 출력하는 프로그램을 작성
      
print("***Q3***")
      
#Q4 레코드가 여러개 있는 FASTA 파일을 임의로 생성하여 각 레코드의 염기 개수>    를 세는 프로그램을 작성
                                                                            
print("***Q4***")
      
"""
