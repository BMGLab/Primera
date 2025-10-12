import sys 

from primera.Utils.bedParser import BedRecord 

if __name__ == "__main__":
    
    chrs = [i for i in sys.argv[2].split(",")]

    bedFile = BedRecord.from_file(sys.argv[1])

    targetedFile = bedFile.filter_by_target(chrs)

    targetedFile.as_df.to_csv("target.csv",sep="\t")

    locFile = targetedFile.filter_by_location()
    for _,g in locFile.as_df.groupby("sample_name"):
        print(g)
    locFile.as_df.to_csv("loc.csv",sep="\t")

