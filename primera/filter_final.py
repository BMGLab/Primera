import sys
import csv

input_file = sys.argv[1]
target_chrs = sys.argv[2].strip()
output_file = sys.argv[3]

target_sorted = ",".join(sorted(target_chrs.split(",")))

with open(input_file, "r", newline="") as infile, open(output_file, "w", newline="") as outfile:
    reader = csv.reader(infile, delimiter="\t")
    writer = csv.writer(outfile, delimiter="\t")
    
    for row in reader:
        if len(row) > 1:
            row_chr_sorted = ",".join(sorted(row[1].split(",")))
            if row_chr_sorted == target_sorted:
                writer.writerow(row)
