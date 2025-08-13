import sys
import pandas as pd

input_file = sys.argv[1]
output_file = sys.argv[2]

rows = []
template_url = "https://genome.ucsc.edu/cgi-bin/hgPcr?hgsid=2900325362_8e48BzUFKDYcxxsPnAlLNmzHKyGA&org=Human&db=hg38&wp_target=genome&wp_f={f}&wp_r={r}&Submit=Submit&wp_size=300&wp_perfect=15&wp_good=15&boolshad.wp_flipReverse=0&wp_append=on&boolshad.wp_append=0"

with open(input_file, "r") as infile:
    for line in infile:
        parts = line.strip().split("\t")
        if len(parts) < 4:
            continue
        with open(f"{parts[1]}_reversed.fa","r") as f:
            headers = []
            segs = []

            for line in f:

                if line.startswith(">"):

                    headers.append(line)

                else:

                    segs.append(line)


            
        forward = parts[4]
        reverse = parts[5]
        url = template_url.format(f=forward, r=reverse)
        rows.append(parts + [url] + [",".join(headers)] + [",".join(segs)])

pd.DataFrame(rows).to_csv(output_file, index=False, header=False,sep="\t")
