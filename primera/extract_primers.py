import os
import sys

def extract_primer_pairs():
    primer_pairs = []
    sequence_id = None
    primleft, primright = None, None
    
   
    for file_name in sys.argv[2:]:
        file_path = os.path.join(file_name)
        
        with open(file_path, "r") as files:
            for line in files:
                line = line.strip()
                
                if line.startswith("SEQUENCE_ID="):
                    sequence_id = line.split('=')[-1].strip()
                elif line.startswith("PRIMER_LEFT_") and "_SEQUENCE" in line:
                    primleft = line.split('=')[-1].strip()
                elif line.startswith("PRIMER_RIGHT_") and "_SEQUENCE" in line:
                    primright = line.split("=")[-1].strip()
                    
                    if primleft and primright and sequence_id:
                        primer_pairs.append((sequence_id, primleft, primright))
                        primleft, primright = None, None
    
    return primer_pairs

def write_primer_pairs(primer_pairs, output_file):
    with open(output_file, 'w') as out:
        
        for idx, (seq_id, forward, reverse) in enumerate(primer_pairs, 1):
            out.write(f"PRIMER_{idx}\t{forward}\t{reverse}\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 extract_primers.py <output_file> <input_file1> [input_file2] ...")
        sys.exit(1)

    output_file = sys.argv[1]
    
    primer_pairs = extract_primer_pairs()
    write_primer_pairs(primer_pairs, output_file)
    
    print(f"Total {len(primer_pairs)} primer pairs extracted to {output_file}") 