import sys
import csv

input_file = sys.argv[1]
target_chrs = sys.argv[2].strip()
output_file = sys.argv[3]

target_sorted = ",".join(sorted(target_chrs.split(",")))

with open(input_file, "r", newline="") as infile, open(output_file, "w", newline="") as outfile:
    reader = csv.reader(infile, delimiter="\t")
    for row in reader:
        if len(row) > 1:
            row_chr_sorted = ",".join(sorted(row[1].split(",")))
            chrDict = {}
            if row_chr_sorted == target_sorted:
                for i, j in enumerate(row[1].split(",")):
                    if j in chrDict:
                        chrDict[j].append(row[i+4])
                    else:
                        chrDict[j] = [row[i+4]]
                
                newChrs = sorted(row[1].split(","))
                a = ""
                for k in newChrs:
                    for l in chrDict[k]:
                        a += f"{l}\t"

                    print(a)
                outfile.write(f"{row[0]}\t{",".join(newChrs)}\t{row[2]}\t{row[3]}\t{a}\n")
                

