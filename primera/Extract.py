import sys
from Bio.Seq import Seq
import os


base_name = os.path.basename(sys.argv[1])[:-17]
seq1, seq2 = base_name.split("+")


fileName1 = f"{seq1}_{seq2}.bl"
fileName2 = f"{seq2}_{seq1}.bl"

def matchLocations(buff1, buff2):
    with open(sys.argv[1], "r") as f:
        with open(fileName1, "w") as sw1:
            with open(fileName2, "w") as sw2:
                f.readline()  
                data = f.readline().split()

                while data:
                    s1, e1, s2, e2 = data

                    # Ref 
                    if int(s1) > int(e1):
                        s1, e1 = e1, s1
                        seq = Seq(buff1[int(s1)+1:int(e1)+1]).reverse_complement()
                        sw1.write(f">{seq1}_{s1}_{e1}|{seq2}_{s2}_{e2}\n{seq}\n")
                    else:
                        sw1.write(f">{seq1}_{s1}_{e1}|{seq2}_{s2}_{e2}\n{buff1[int(s1)+1:int(e1)+1]}\n")

                    # Query seq
                    if int(s2) > int(e2):
                        s2, e2 = e2, s2
                        seq = Seq(buff2[int(s2)+1:int(e2)+1]).reverse_complement()
                        sw2.write(f">{seq2}_{s2}_{e2}|{seq1}_{s1}_{e1}\n{seq}\n")
                    else:
                        sw2.write(f">{seq2}_{s2}_{e2}|{seq1}_{s1}_{e1}\n{buff2[int(s2)+1:int(e2)+1]}\n")

                    data = f.readline().split()


with open(f"{sys.argv[2]}/{seq1}", "r") as f1:
    f1.readline()  
    buff1 = f1.read().replace("\n", "")


with open(f"{sys.argv[2]}/{seq2}", "r") as f2:
    f2.readline()  
    buff2 = f2.read().replace("\n", "")


matchLocations(buff1, buff2)
