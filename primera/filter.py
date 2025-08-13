import pandas as pd
import sys
import py2bit
from Bio.Seq import Seq


def parse_csv_file(psl_file, allowed_chr_list):
    
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


if __name__ == "__main__":
    pslFile = sys.argv[1]
    chr_input = sys.argv[2]
    twoBit = sys.argv[3]

    tbitFile = py2bit.open(twoBit)
    
    allowed_chr = set([c.strip() for c in chr_input.split(",")])

    filesToParse = set()
    
    seqList = parse_csv_file(pslFile, allowed_chr)

    for segid, i in enumerate(seqList):
        with open(f"seg_{segid}_original.fa","w") as f:
            with open(f"seg_{segid}_reversed.fa","w") as f1:
                fDict = {}
                f1Dict = {}
                for k,j in enumerate(i[1]):

                    sequence = Seq(tbitFile.sequence(str(j),int(i[2][k]),int(i[3][k])))
                    
                    sequence1 = sequence 
                    
                    if i[4][k] == "-":
                        sequence1 = sequence.reverse_complement()
                   
                    #TODO: DELETE HERE WHEN WE FIX THE DUPLICATE NAMES STUFF IN THE PSL FILE
                    if j not in fDict and j not in f1Dict:
                        fDict[j] = sequence
                        f1Dict[j] = sequence1
                    
                    f.write(f">{j}_{int(i[2][k])}_{int(i[3][k])}\n{sequence}\n")
                    f1.write(f">{j}_{int(i[2][k])}_{int(i[3][k])}\n{sequence1}\n")
