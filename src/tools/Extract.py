import sys
from Bio.Seq import Seq
from pyfaidx import Fasta


locations_file = sys.argv[1]
base_name = locations_file.split("/")[-1]


if not base_name.endswith(".locations"):
    sys.exit(f"Error: Expected a .locations file, but got {base_name}")
core_name = base_name[:-10] # Remove ".locations"


file_parts = core_name.split("+")

if len(file_parts) == 2:
    
    seq1_filename = file_parts[0]
    seq2_filename = file_parts[1]
else:
    
    seq1_filename = file_parts[0]
    seq2_filename = file_parts[0] 

fileName1 = seq1_filename[:-2] + "_"  + seq2_filename[:-2] +"_ext_0" + ".fa" #TODO .fa(-2) or .fa.masked(-9)
fileName2 = seq2_filename[:-2] + "_"  + seq1_filename[:-2] +"_ext_1"+ ".fa"

def matchLocations(sequences1, sequences2, seq1_id, seq2_id):


    with open(sys.argv[1],"r") as f:
        with open(fileName1,"w") as sw1:
            with open(fileName2,"w") as sw2:
 
                f.readline()
            
                data = f.readline().split()

                while data:
                    s1, e1, s2, e2 = map(int, data)
                 
                    start1, end1 = s1, e1

                    if start1  > end1 :
                        start1, end1 = end1, start1
                        seq = sequences1[seq1_id][start1-1:end1].reverse.complement
                        sw1.write(f">{seq1_id}_{start1}_{end1}_{seq2_id}_{s2}_{e2}\n{seq.seq}\n")
                    else:
                        seq = sequences1[seq1_id][start1-1:end1]
                        sw1.write(f">{seq1_id}_{start1}_{end1}_{seq2_id}_{s2}_{e2}\n{seq.seq}\n")
                    
                    start2, end2 = s2, e2

                    if  start2 > end2 :
                        
                        start2, end2 = end2, start2
                        seq = sequences2[seq2_id][start2-1:end2].reverse.complement
                        sw2.write(f">{seq2_id}_{start2}_{end2}_{seq1_id}_{s1}_{e1}\n{seq.seq}\n")
                        
                    else:
                        seq = sequences2[seq2_id][start2-1:end2]
                        sw2.write(f">{seq2_id}_{start2}_{end2}_{seq1_id}_{s1}_{e1}\n{seq.seq}\n")
     
                    data = f.readline().split()

def main():                                                        
    sequences1 = Fasta(f"{sys.argv[2]}/{seq1_filename}")
    sequences2 = Fasta(f"{sys.argv[2]}/{seq2_filename}")
    
    seq1_id = seq1_filename.replace(".fa.masked", "")
    if seq1_id not in sequences1:
        seq1_id = list(sequences1.keys())[0]

    seq2_id = seq2_filename.replace(".fa.masked", "")
    if seq2_id not in sequences2:
        seq2_id = list(sequences2.keys())[0]
    
    
    matchLocations(sequences1, sequences2, seq1_id, seq2_id)