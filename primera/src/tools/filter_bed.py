import sys
from dataclasses import dataclass
import pandas as pd

@dataclass
class Primer_Pair:
    
    _id: str
    forward: str
    reverse: str
    chrs: dict

def main():
    template_url = "https://genome.ucsc.edu/cgi-bin/hgPcr?hgsid=2900325362_8e48BzUFKDYcxxsPnAlLNmzHKyGA&org=Human&db=hg38&wp_target=genome&wp_f={f}&wp_r={r}&Submit=Submit&wp_size=300&wp_perfect=15&wp_good=15&boolshad.wp_flipReverse=0&wp_append=on&boolshad.wp_append=0"
    input_bed = sys.argv[1]
    input_primers = sys.argv[2]
    target_chrs = sys.argv[3]

    target_sorted = target_chrs.split(",")
    target_sorted.sort()

    primer_sequences = {}
    with open(input_primers) as f:
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) >= 3:
                primer_id = fields[0]
                forward = fields[1]
                reverse = fields[2]
                primer_sequences[primer_id] = (forward, reverse)

    primer_pairs = {}
    with open(input_bed) as f:
        for line in f:
            fields = line.strip().split()
            if len(fields) < 4:
                continue
            key = fields[3] 
            chrom = fields[0]
            loc = fields[1]
            forward,reverse = primer_sequences[key]
            id_ = f"{key.split("_")[0]}_{key.split("_")[1]}"

            if key in primer_pairs:

                primer_pairs[key].chrs[chrom] = loc

            else:
                newPrimerPair = Primer_Pair(id_, forward, reverse, {chrom: loc})
                primer_pairs[key] = newPrimerPair

    cols = ["id","chrs","locs","first","forward","reverse","url","seg_ids","segs"]
    df = pd.DataFrame(columns = cols)


    for i in primer_pairs:
        pair = primer_pairs[i]
        chrs_sorted = list(pair.chrs.keys())
        chrs_sorted.sort()
        
        df_chrs = ""
        df_locs = ""
        if chrs_sorted == target_sorted:
            for i in chrs_sorted:

                df_chrs += f",{i}"
            
                df_locs += f",{pair.chrs[i]}"

            
            first = df_locs.split(",")[1]


            with open(f"{pair._id}_reversed.fa","r") as f:
                        headers = ""
                        segs = ""

                        for line in f:

                            if line.startswith(">"):

                                headers += f",{line}"

                            else:

                                segs += f",{line}"

            url = template_url.format(f=pair.forward, r=pair.reverse)
            headers,segs = headers[1:],segs[1:]

            df.loc[len(df)] = [pair._id, df_chrs[1:], df_locs[1:], first ,pair.forward, pair.reverse, url, headers, segs]

    df.sort_values(by="first",inplace=True,ascending=True)

    newDfList = []

    threshold = 18

    num = int(df.iloc[0,3]) - 18 - 1

    for i,j in enumerate(df.iloc[:,3]):
        j = int(j)
        if j - num >= threshold:
            num = j
            newDfList.append(df.iloc[i,:])
            
    df = df.drop('first', axis=1)

    df2 = pd.DataFrame(newDfList,columns=df.columns)

    df2.to_csv("results.csv",sep="\t",header=False,index=False)
