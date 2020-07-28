#! /usr/bin/env python
# -*- coding: utf-8 -*-

#0727 Computing GC content

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


"""
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
"""
