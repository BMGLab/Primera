import pandas as pd

def parser(psl_path, chr_list, output_txt):
    cols = [
        "match", "mis-match", "rep-match", "N's", "Q gap count", "Q gap bases",
        "T gap count", "T gap bases", "strand",
        "Q name", "Q size", "Q start", "Q end",
        "T name", "T size", "T start", "T end",
        "block count", "blockSizes", "qStarts", "tStarts"
    ]

    df = pd.read_csv(psl_path, sep="\t", header = None, names = cols, skiprows=4)
    grouped = df.groupby("Q name")

    with open(output_txt, "w") as out:
        for group_name, group_df in grouped:
            t_names = set(group_df["T name"].unique())

            if t_names == (chr_list):
                out.write(f"{group_name}\n")

if __name__ == "__main__":
    import sys
    psl_file = sys.argv[1]
    chrs = set(sys.argv[2].split(","))
    output_txt = sys.argv[3]
    parser(psl_file, chrs, output_txt)
