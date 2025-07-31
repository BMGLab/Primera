import pandas as pd

def parser(psl_path, chr_list):
    cols = [
        "match", "mis-match", "rep-match", "N's", "Q gap count", "Q gap bases",
        "T gap count", "T gap bases", "strand",
        "Q name", "Q size", "Q start", "Q end",
        "T name", "T size", "T start", "T end",
        "block count", "blockSizes", "qStarts", "tStarts"
    ]

    df = pd.read_csv(psl_path, sep="\t", header = None, names = cols, skiprows=4)

    grouped = df.groupby("Q name")

    print("\nRESULTS :", chr_list), "\n"

    for group_name, group_df in grouped:
        t_names = set(group_df["T name"].unique())
        if t_names.issubset(chr_list):
            print(f"#Group: {group_name}")
            print(group_df.to_string(index=False))
            print()

if __name__ == "__main__":
    psl_file = input("Enter PSL file path: ").strip()
    chr_input = input("Enter chrs: ").strip()

    chrs = set(c.strip() for c in chr_input.split(",") if c.strip())

    parser(psl_file, chrs)
