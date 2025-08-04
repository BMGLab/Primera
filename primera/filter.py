import pandas as pd
import sys

def parse_csv_file(psl_file, allowed_chr_list):
    
    seqList = []

    columns = [
    "match", "mis-match", "rep-match", "N's", "Q gap count", "Q gap bases",
    "T gap count", "T gap bases", "strand",
    "Q name", "Q size", "Q start", "Q end",
    "T name", "T size", "T start", "T end",
    "block count", "blockSizes", "qStarts", "tStarts"]
    
    df = pd.read_csv(psl_file, sep='\t', header=None, names=columns, skiprows=4)

    df = df.sort_values("Q name")


    if "Q name" not in df.columns or "T name" not in df.columns:
        print("error!")
        return

    grouped = df.groupby("Q name")

    for group_name, group_df in grouped:
        
        t_names = set(group_df["T name"].unique())
        
        if len(t_names) ==1 and len(allowed_chr_list) != 1:
            continue
        
        if t_names == allowed_chr_list:
            seqList.append(group_name)
    
    return seqList


if __name__ == "__main__":
    pslFile = sys.argv[1]
    chr_input = sys.argv[2]

    allowed_chr = set([c.strip() for c in chr_input.split(",")])
    
    filesToParse = set()
    
    print(parse_csv_file(pslFile, allowed_chr))
     #   fileName = ''.join(k for k in i.split("_")[:-2])

      #  filesToParse.add(fileName)
