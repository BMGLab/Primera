from Bio import SeqIO
import sys

fasta_path = sys.argv[1]
id_path = sys.argv[2]
output_path = sys.argv[3]

with open(id_path) as f:
    wanted_ids = set(line.strip() for line in f)

records = (r for r in SeqIO.parse(fasta_path, "fasta") if r.id in wanted_ids)
SeqIO.write(records, output_path, "fasta")
