
import sys
import json

def read_txt(file_name:str)->str:
    ret=""
    with open(file_name,'r') as handle:
        for line in handle:
            if line.startswith(">"):
                continue
            ret += line.strip()
    return ret

if __name__=="__main__" :
    if len(sys.argv) !=2:
        print("#usage: python {sys.argv[0]} [txt]")
        sys.exit()

    file_name=sys.argv[1]
    txt=read_txt(file_name)
    print(txt)

#리스트 안에 딕셔너리
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

def read_tsv(file_name:str)->list:
    ret=[]
    with open(file_name,'r') as handle:
        for line in handle:
            if line.startswith("#"):
                header=line.strip().split("\t")
                continue
            splitted=line.strip().split("\t")
            d=dict(zip(header, splitted))
            ret.append(d)
    return ret


def read_tsv(file_name:str)->list:
    ret=[]
    with open(file_name,'r') as handle:
        for line in handle:
            if line.startswith("#"):
                header=line.strip().split("\t")
                continue
            splitted=line.strip().split("\t")
            d=dict(zip(header, splitted))
            ret.append(d)
    return ret

def to_json(l :list) -> None:
    with open("read_sample.json","w") as handle:
        json.dump(l, handle, indent=4)

if __name__=="__main__" :
    if len(sys.argv) !=2:
        print("#usage: python {sys.argv[0]} [txt]")
        sys.exit()

    file_name=sys.argv[1]
    ret=read_csv(file_name)
    print(ret)
    to_json(ret)
