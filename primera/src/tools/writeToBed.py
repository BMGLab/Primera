import sys

def main():
    with open(sys.argv[1],"r") as f1, open(sys.argv[2],"w") as f2:
        for line in f1:
            
            l = line.split("\t")
            for i in range(len(l[1].split(","))):
                f2.write(f"{l[1].split(",")[i]}\t{l[2].split(",")[i]}\t{l[3].split(",")[i]}\n") 
                         
