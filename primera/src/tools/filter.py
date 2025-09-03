import pandas as pd
import sys
import py2bit
from Bio.Seq import Seq
import argparse


def parse_csv_file(psl_file, allowed_chr_list,hard_filter):
    
    seqList = []

    columns = [
    "match", "mis-match", "rep-match", "N's", "Q gap count", "Q gap bases",
    "T gap count", "T gap bases", "strand",
    "Q name", "Q size", "Q start", "Q end",
    "T name", "T size", "T start", "T end",
    "block count", "blockSizes", "qStarts", "tStarts"]
    
    df = pd.read_csv(psl_file, sep='\t', header=None, names=columns, skiprows=4)
    df = df[~df["T name"].str.contains("_", na=False)]

    df = df.sort_values("Q name")

    if "Q name" not in df.columns or "T name" not in df.columns:
        print("error!")
        return

    grouped = df.groupby("Q name")

    for group_name, group_df in grouped:

        if hard_filter:
            t_names = list(group_df["T name"])
            t_names.sort()
        else:
            t_names = set(group_df["T name"].unique())
        
        if len(t_names) == 1 and len(allowed_chr_list) != 1:
            continue
        
        if t_names == allowed_chr_list:
            seqList.append([group_name,
                            group_df["T name"].values,
                            group_df["T start"].values,
                            group_df["T end"].values,
                            group_df["strand"].values]
                           )
    return seqList


def main():
    
    parser = argparse.ArgumentParser(description = "FilterPsl")

    parser.add_argument("-p","--pslFile",
                        help = "Path to .psl file"
                        )

    parser.add_argument("-c","--chrs",
                        help = "Filtered chrs")

    parser.add_argument("-t","--tbitfile",
                        help = "TwoBit File Path")

    parser.add_argument("--soft-filter",action="store_true",
                        help = "Use soft filtering, may help getting slightly more results or useful if you want less specifity, but increases filtering time drastically. Read the documentation for more info.")
    
    args = parser.parse_args()
    
    pslFile = args.pslFile
    chr_input = args.chrs
    twoBit = args.tbitfile

    if pslFile == None or chr_input == None or twoBit == None:
        print("Arguments can't be empty!")
        exit()

    if args.soft_filter == False:
        
        allowed_chr = [c.strip() for c in chr_input.split(",")]
        allowed_chr.sort()

        hard_filter = True

    else:
        
        hard_filter = False

        allowed_chr = set([c.strip() for c in chr_input.split(",")])



    tbitFile = py2bit.open(twoBit)
     
    seqList = parse_csv_file(pslFile, allowed_chr, hard_filter)

    for segid, i in enumerate(seqList):
        with open(f"seg_{segid}_original.fa","w") as f:
            with open(f"seg_{segid}_reversed.fa","w") as f1:

                for k,j in enumerate(i[1]):

                    sequence = Seq(tbitFile.sequence(str(j),int(i[2][k]),int(i[3][k])))
                    
                    sequence1 = sequence 

                    if i[4][k] == "-":
                        sequence1 = sequence.reverse_complement()
                    

                    f.write(f">{j}_{int(i[2][k])}_{int(i[3][k])}\n{sequence}\n")
                    f1.write(f">{j}_{int(i[2][k])}_{int(i[3][k])}\n{sequence1}\n")
