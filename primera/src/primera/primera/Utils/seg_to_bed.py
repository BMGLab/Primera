# TODO : This code is veeeeery ugly. Use pandas to optimize this. Not that important but still.
def segToBed(filepath, outfile):
    with open(filepath ,"r") as f1, open(outfile,"w") as f2:

        f1.readline()
        # For the header.
        for line in f1:
            
            l = line.split("\t")
            
            for i in range(len(l[1].split(","))):
                f2.write(f"{l[1].split(",")[i]}\t{l[2].split(",")[i]}\t{l[3].split(",")[i]}\n")  
