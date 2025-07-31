import pandas as pd

def parse_csv_file(csv_path, allowed_chr_list):
    df = pd.read_csv(csv_path, comment='#')  

    if "Q name" not in df.columns or "T name" not in df.columns:
        print("error!")
        return

    grouped = df.groupby("Q name")

    print("\n RESULTs(only this chr's:", allowed_chr_list, ")\n")

    for group_name, group_df in grouped:
        t_names = set(group_df["T name"].unique())
        if t_names.issubset(allowed_chr_list):
            print(f"# Group: {group_name}")


if __name__ == "__main__":
    csv_file = input(" enter csv filepath: ").strip()
    chr_input = input(" want chrs(ex: chr3,chr7,chr8): ").strip()

    allowed_chr = set([c.strip() for c in chr_input.split(",") if c.strip()])

    parse_csv_file(csv_file, allowed_chr)
