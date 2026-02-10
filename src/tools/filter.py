import pandas as pd
import argparse
import py2bit
import sys
from Bio.Seq import Seq

def parsePsl(psfFile, allowed_chr_list, mode):
    seqList = []

    columns = [
        "match", "mis-match", "rep-match", 
        "N's", "Q gap count", "Q gap bases",
        "T gap count", "T gap bases", "strand",
        "Q name", "Q size", "Q start", "Q end",
        "T name", "T size", "T start", "T end",
        "block count", "blockSizes", "qStarts", "tStarts"
    ]

    subColumns  = ["Q name", "T name", "T start", "T end", "strand"]

    dtypes      = {"Q name" : "string", 
                   "T name" : "category", 
                   "strand" : "category", 
                   "T start": "int32", 
                   "T end"  : "int32"}


    df = pd.read_csv(psfFile, 
                     sep="\t", 
                     names=columns,
                     usecols=subColumns ,
                     dtype=dtypes, 
                     header=None, 
                     skiprows=5, 
                     low_memory=False)
    
    
    df = df.sort_values("Q name")

    if "Q name" not in df.columns or "T name" not in df.columns:
        print("Error: PSL columns not found.")
        sys.exit(1)

    grouped = df.groupby("Q name")
    for group_name, group_df in grouped:
        t_names = set(group_df["T name"].unique())

        if mode == "strict":
            if t_names == set(allowed_chr_list):
                seqList.append([
                    group_name,
                    group_df["T name"].values,
                    group_df["T start"].values,
                    group_df["T end"].values,
                    group_df["strand"].values,     
                ])

        elif mode == "contain":
            if set(allowed_chr_list).issubset(t_names):
                seqList.append([
                    group_name,
                    group_df["T name"].values,
                    group_df["T start"].values,
                    group_df["T end"].values,
                    group_df["strand"].values,     
                ])

        else:
            print(f"Error: Unknown mode '{mode}'. Use 'strict' or 'contain'.")
            sys.exit(1)
    return seqList

def main():
    parser = argparse.ArgumentParser(description="Filter sequences based on PSL alignment.")

    parser.add_argument("-p", "--pslFile", required=True, help="Input PSL file.")
    parser.add_argument("-c", "--chrs", required=True, help="Comma-separated list of allowed chromosomes.")
    parser.add_argument("-t", "--tbitfile", required=True, help="Input 2bit file.")
    parser.add_argument("--mode", choices=["strict", "contain"], default="strict", help="Filtering mode: 'strict' or 'contain'. Default is 'strict'.")

    args = parser.parse_args()


  
    pslFile     = args.pslFile
    chr_input   = args.chrs
    twoBitFile  = args.tbitfile
    mode        = args.mode

    allowedChr = [c.strip() for c in chr_input.split(",")]

    try:
        tbitFile = py2bit.open(twoBitFile)
    except Exception as e:
        print(f"2bit file error: {e}")
        sys.exit(1)
    
    seqList = parsePsl(pslFile, allowedChr, mode)

    if not seqList:
        print(f"error : not find result with filter options")
        sys.exit(0)

    for segID, i in enumerate(seqList):
        with open(f"seg_{segID}_original.fa", "w") as f:
            with open(f"seg_{segID}_reversed.fa", "w") as f1:
                for k, j in enumerate(i[1]):
                    
                    sequence = Seq(tbitFile.sequence(str(j), int(i[2][k]), int(i[3][k])))
                    sequence_rc = sequence.reverse_complement() if i[4][k] == "-" else sequence

                    newID = f"seg{segID}_{j}_{int(i[2][k])}_{int(i[3][k])}"
                    f.write(f">{newID}\n{sequence}\n")
                    f1.write(f">{newID}\n{sequence_rc}\n")

if __name__ == "__main__":
    main()
                  

