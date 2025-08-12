import sys

input_bed = sys.argv[1]
input_primers = sys.argv[2]
output_file = sys.argv[3]

primer_sequences = {}
with open(input_primers) as f:
    for line in f:
        fields = line.strip().split('\t')
        if len(fields) >= 3:
            primer_id = fields[0]
            forward = fields[1]
            reverse = fields[2]
            primer_sequences[primer_id] = (forward, reverse)


chroms = {}

locs = {}

with open(input_bed) as f:
    for line in f:
        print(line)
        fields = line.strip().split()
        if len(fields) < 4:
            continue
        key = fields[3] 
        value = fields[0]
        
        if key in locs:
            locs[key].append(fields[1])
        else:
            locs[key] = [fields[1]]
        
        if key in chroms:
            chroms[key].append(value)
        else:
            chroms[key] = [value]


with open(output_file, 'w') as out:
    for key in sorted(chroms):
        if key in primer_sequences:
            forward, reverse = primer_sequences[key]
            out.write(f"{key}\t{','.join(chroms[key])}\t{forward}\t{reverse}\t{"\t".join(locs[key])}\n")
        else:
            out.write(f"{key}\t{','.join(chroms[key])}\tN/A\t\n")
