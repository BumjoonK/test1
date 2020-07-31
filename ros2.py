#! /usr/bin/env python
# -*- coding: utf-8 -*-

#0727 Computing GC content
"""
import sys

def GCcontent(file_name):
    ret={}
    with open(file_name, 'r') as handle:
        for line in handle:
            if line.startswith(">"):
                header=line.strip()
                continue
            elif header in ret:
                ret[header] += line.strip()
            else:
                ret[header] = line.strip()
    return ret

file_name=sys.argv[1]
result = GCcontent(file_name)
print(result) 

#value 값의 GC-content 값을 계산한뒤 가장 높은 GC-content
"""
#1. 딕셔너리 형태로 분리하기
ret = {}
with open("GCcontent.fa",'r') as handle:
    for line in handle:
        if line.startswith(">"):
            header=line.strip()
            continue
        elif header in ret:
            ret[header] += line.strip()
        else:
            ret[header] = line.strip()
        
print(ret)

#value 값의 GC-content 값을 계산한뒤 가장 높은 GC-content

dic_rate = {} # id와 GC비율 저장 딕셔너리  
for key, value in ret.items():
    base_cnt = 0 #base_cnt 초기화
    for base in value:  #
        if base == "C" or base == "G":
            base_cnt += 1
    a =float(base_cnt)/len(value)*100
    dic_rate[key] = a #CG비율을 value로 할당

print(dic_rate)

max_id,max_rate ="", 0
for key, value in dic_rate.items():
    if max_rate<value:
        max_rate = value
        max_id = key
print("max id",max_id, "max rate", max_rate)
            
    






