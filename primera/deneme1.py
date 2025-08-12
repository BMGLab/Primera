import sys
import pandas as pd

threshold = 3

bedFile = sys.argv[1]
input_primers = sys.argv[2]

primer_sequences = {}
with open(input_primers) as f:
    for line in f:
        fields = line.strip().split('\t')
        if len(fields) >= 3:
            primer_id = fields[0]
            forward = fields[1]
            reverse = fields[2]
            primer_sequences[primer_id] = (forward, reverse)

columns = ["chr","start","end","sample_name","score","strand"]
df = pd.read_table(bedFile,sep="\t",names=columns)
df["Primers"] = None
newColumns = ["chr","start","end","sample_name","score","strand","Primers"]

for i in range(len(df)):

    sample = df.iloc[i, 3]
    try:
        val = f"{primer_sequences[sample][0]},{primer_sequences[sample][1]}"
    except KeyError:
        val = "N/A"
    df.loc[i, "Primers"] = val

grouped = df.groupby("chr")


df2 = pd.DataFrame(columns=newColumns)


for groupName, groupdf in grouped:
    
    groupdf = groupdf.sort_values(by="start",ascending=True)
    
    num = groupdf.iloc[0,1] - threshold - 1

    for i,j in enumerate(groupdf.iloc[:,1]):
        if j - num > threshold:
            num = j
            df2.loc[len(df2)] = groupdf.iloc[i]

grouped = df2.groupby("Primers")

for groupName, groupdf in grouped:
    a = ",".join(sorted(groupdf.iloc[:,0].values))
    #print(sorted(groupdf.iloc[:,0].values))

    if a == "chr13,chr18,chr21":
        print(f"{groupName}\t{a}")
