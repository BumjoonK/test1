#Fasta file A,C,G,T 개수, Class 사용
import sys

class FASTA:
    def __init__(self,file_name:str):
        self.file_name=file_name
        self.count={}
        self.length=0
    def count_base(self):
        with open(self.file_name,"r") as handle:
            for line in handle:
                if line.startswith(">"):
                    continue
            line=line.strip()
            for s in line:
                if s in self.count:
                    self.count[s] += 1
                else:
                    self.count[s] = 1
    """
    #대화형 파이썬으로 결과 보기
    import tool
    t = tool.FASTA("059.fasta")
    t
    #<tool.FASTA object at 0x104b038d0>
    dir(t)
    #['__class__','__delattr__', ...]
    t.count_base()
    tcount
    #{'A':497,'T':514, 'C':444,'G':585}
    """
    def __len__(self):
        for k,v in self.count.items():
            self.length += v
        return self.length

#네 줄이 하나의 리드를 구성할 때 1st 헤더 2 nd 서열 3 rd 구분자 + 4 th quality

class FASTQ:
    def __init__(self, file_name):
        self.file_name = file_name
        self.read_num=0
        self.base ={}
    def count_read_num(self):
        cnt=0
        with open(self.file_name, 'r') as handle:
            for line in handle:
                if cnt % 4 == 0:
                    header = line.strip()
                    self.read_num += 1
                elif cnt % 4 == 1:
                    seq = line.strip()
                    for s in seq:
                        if s in self.base:
                            self.base[s] += 1
                        else:
                            self.base[s] =1
                elif cnt % 4 == 3:
                    qual = line.strip()
                cnt +=1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"#usage:python {sys.argv[0]}[fasta]")
        sys.exit

    file_name = sys.argv[1]
    """
    t = FASTA(file_name)
    t.count_base()
    t=FASTA(file_name)
    t.count_read_num()
    print(t.read.num)
    print(t.count)
    print(t.length)
    print(len(t))
    """
    t = FASTQ(file_name)
    t.count_read_num()
    print(t.read_num)
    print(t.base)
#VCF(Variant Calling Format)_변이 정보 표기 메타데이터"##" 헤더와 변이 위치 "#"



