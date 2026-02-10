import sys

def processRecord(results):
    try:
        num_primers_found = int(results.get('PRIMER_PAIR_NUM_RETURNED', 0))
    except ValueError:
        num_primers_found = 0

    sequenceID          = results.get('SEQUENCE_ID', 'unknown_sequence')
    full_template       = results.get('SEQUENCE_TEMPLATE', 'NA')

    if num_primers_found > 0:
        for i in range(num_primers_found):
            left_primer_seq     = results.get(f'PRIMER_LEFT_{i}_SEQUENCE', 'NA')
            right_primer_seq    = results.get(f'PRIMER_RIGHT_{i}_SEQUENCE', 'NA')
            
            # Probe
            probe_seq           = results.get(f'PRIMER_INTERNAL_OLIGO_{i}_SEQUENCE', 'NA')
            probe_tm            = results.get(f'PRIMER_INTERNAL_OLIGO_{i}_TM', 'NA')
            probe_gc            = results.get(f'PRIMER_INTERNAL_OLIGO_{i}_GC_PERCENT', 'NA')

            l_coord_raw = results.get(f'PRIMER_LEFT_{i}', '0,0').replace('[','').replace(']','').replace(' ','')
            r_coord_raw = results.get(f'PRIMER_RIGHT_{i}', '0,0').replace('[','').replace(']','').replace(' ','')

            left_coords  = l_coord_raw.split(',')
            right_coords = r_coord_raw.split(',')

            amplicon_seq = "NA"
            
            # Subsequence extraction
            if full_template != "NA" and len(left_coords) >= 2 and len(right_coords) >= 2:
                try:
                    l_start = int(left_coords[0])

                    r_start = int(right_coords[0]) 
                    
                    
                    amplicon_seq = full_template[l_start : r_start + 1]
                except ValueError:
                    amplicon_seq = full_template 
            
            primer_pair_name = f"{sequenceID}_pair_{i}"
            
            print(f"{primer_pair_name}\t{left_primer_seq}\t{right_primer_seq}\t{amplicon_seq}\t{probe_seq}\t{probe_tm}\t{probe_gc}")

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Error: No input file provided.\n")
        sys.exit(1)
    
    file_path = sys.argv[1]
    current_record = {}

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if line == '=':
                processRecord(current_record)
                current_record = {}
            elif '=' in line:
                # split only on the first '='
                key, value = line.split('=', 1)
                current_record[key] = value

if __name__ == '__main__':
    main()