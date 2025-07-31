import pandas as pd

psl_file = "/home/user/"
output_file = "/home/user"

columns = [
    "match", "mis-match", "rep-match", "N's", "Q gap count", "Q gap bases",
    "T gap count", "T gap bases", "strand",
    "Q name", "Q size", "Q start", "Q end",
    "T name", "T size", "T start", "T end",
    "block count", "blockSizes", "qStarts", "tStarts"
]

df = pd.read_csv(psl_file, sep='\t', header=None, names=columns, skiprows=4)

df = df.sort_values("Q name")

with open(output_file, "w") as f:
    for qname, group in df.groupby("Q name"):
        f.write(f"# Group: {qname}\n")  
        group.to_csv(f, index=False, header=True)  
        f.write("\n")  
