import sys

from primera.Utils.pslParser import PslRecord

chrs = sys.argv[2].split(",")

print("PslRecord Object Creating...")
psl_record = PslRecord.from_file(sys.argv[1])

print("filter_by_target()...")
filtered_record = psl_record.filter_by_target(chrs, hard_filter=False)

filtered_record.as_df.to_csv("filteredPsl.csv", sep = "\t")

print("fill_spaces()...")
filtered_record.fill_spaces()

filtered_record.as_df.to_csv("filledPsl.csv", sep = "\t")

print("Writing Files...")

segments = filtered_record.extract_groups(sys.argv[3],reverse_complement=False)
segments_reversed = filtered_record.extract_groups(sys.argv[3],reverse_complement=True)

for idx,seg in enumerate(segments):

    seg.to_file(f"seg_{idx}.fa")

for idx, seg_r in enumerate(segments_reversed):

    seg_r.to_file(f"seg_{idx}_reversed.fa")


print("Nice!")
