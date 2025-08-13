import pandas as pd 
import sys

threshold = 18

df = pd.read_csv(sys.argv[1],sep="\t",header=None)
print(df)

df2 = pd.DataFrame(columns=df.columns)

df.sort_values(by=5,inplace=True, ascending=True)

num = df.iloc[0,5] - threshold - 1
print(type(num))

for i,j in enumerate(df.iloc[:,5]):
    if j - num >= threshold:
        num = j
        df2.loc[len(df2)] = df.iloc[i,:5]

print(df2)
df2.to_csv("last.csv",sep="\t", header=False) 


