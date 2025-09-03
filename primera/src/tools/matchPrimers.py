import sys
from Bio.Seq import Seq


seqList = []

def match_primers(file):
    
    with open(file,"r") as f:

        data = f.read().split("\n")
        buffList = [] 
        primersList = []
        matchedChr = {}
        buff = ""
        for i in data:
            
            if i != "=":
                data = i.split("=")

                if i.split("=")[0][-8:] == "SEQUENCE" and data[0][:11] == "PRIMER_LEFT":
                    
                    buff += data[1].replace("\n","")
                
                elif i.split("=")[0][-8:] == "SEQUENCE" and data[0][:12] == "PRIMER_RIGHT":
                    buff += ","
                    buff += data[1].replace("\n","")
                    
                    buffList.append(buff)
                    
                    buff = ""
                
                elif data[0] == "SEQUENCE_TEMPLATE":

                    seqList.append(Seq(data[1]))
                
                elif data[0] == "SEQUENCE_ID":

                    _id = f"{data[1]}"
            else:
                matchedChr[_id] = buffList
                _id = ""
                buffList = []

    return matchedChr

def main():
    data = match_primers(sys.argv[1])

    seg_id = sys.argv[1].split(".")[0]
        
    a = 0

    for i in data:
        for j in data[i]:
            mapped = True
            fr,rv = j.split(",")
            
            for k in seqList:
                if fr in k and rv in k.reverse_complement():
                    pass
                elif fr in k.reverse_complement() and rv in k:
                    pass
                else:
                    mapped = False

            if mapped:
                print((f"{seg_id}_{i}_{a}\t{fr}\t{rv}\n"))
                a += 1
