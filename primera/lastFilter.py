import pandas as pd 
import sys

threshold = 18

df = pd.read_csv(sys.argv[1],sep="\t",header=None)

df2 = pd.DataFrame(columns=df.columns)

df.sort_values(by=4,inplace=True, ascending=True)

num = df.iloc[0,4] - threshold - 1

for i,j in enumerate(df.iloc[:,4]):
    if j - num >= threshold:
        num = j
        df2.loc[len(df2)] = df.iloc[i]

print(df2)
df2.to_csv("last.csv",sep="\t", header=False) 



