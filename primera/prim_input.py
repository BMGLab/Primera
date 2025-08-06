from Bio import SeqIO
import sys


input_files = sys.argv[1:-1]
output_file = sys.argv[-1]

with open(output_file, 'w') as out:
    for seq_file in input_files:
        record = next(SeqIO.parse(seq_file, "fasta"))
        out.write(f"SEQUENCE_ID={record.id}\n")
        out.write(f"SEQUENCE_TEMPLATE={record.seq}\n")
        out.write("PRIMER_OUTPUT_FORMAT=0\n")
        out.write("PRIMER_TASK=generic\n")
        out.write("PRIMER_PRODUCT_SIZE_RANGE=150-200\n")
        out.write("PRIMER_EXPLORATORY=1\n")
        out.write("PRIMER_NUM_RETURN=30\n")
        out.write("=\n")


