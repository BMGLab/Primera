import primer3
import sys
import argparse
import json
import os


def parseFasta(file_path):
    sequences = []                                                                  #TODO yield 
    current_id = None
    current_seq = []

    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                if line.startswith('>'):
                    if current_id:
                        sequences.append((current_id, ''.join(current_seq)))
                    current_id = line[1:].split()[0]
                    current_seq = []
                else:
                    current_seq.append(line)
            if current_id and current_seq:
                sequences.append((current_id, ''.join(current_seq)))
    except FileNotFoundError:
        return[]

    if not sequences and current_seq:                                                # if not header found, treat entire file as a single sequence
        seq_id = os.path.splitext(os.path.basename(file_path))[0]
        sequences.append((seq_id, "".join(current_seq)))
    
    return sequences

def main():
    
    parser =argparse.ArgumentParser(description="Run Primer3 with config file.")
    parser.add_argument("input_file", help="Input FASTA file")
    parser.add_argument("--config", required=True, help="primerSettings.json ")
    args = parser.parse_args()

    input_file = args.input_file
    config_file = args.config

    try:
        with open(config_file, 'r') as f:
            global_args = json.load(f)
    
    except Exception as e:
        print(f"Error loading config file: {str(e)}")
        sys.exit(1)

    min_product_size = 100
    if "PRIMER_PRODUCT_SIZE_RANGE" in global_args:
        min_product_size = global_args["PRIMER_PRODUCT_SIZE_RANGE"][0][0]

    allSequences = parseFasta(input_file)
    if not allSequences:
        return
    
    baseName        = os.path.splitext(os.path.basename(input_file))[0]
    outputFileName  = f"{baseName}.prim"
    

    with open(outputFileName, 'w') as f:
        for seq_id, seq_template in allSequences:
            if len(seq_template) < min_product_size:
                f.write(f"SEQUENCE_ID={seq_id}\n")
                f.write(f"PRIMER_ERROR=Seq short\n")
                f.write("=\n")
                continue

            seq_args = {
                'SEQUENCE_ID': seq_id,
                'SEQUENCE_TEMPLATE': seq_template
            }

            try:
                results = primer3.design_primers(seq_args, global_args)
                
                f.write(f"SEQUENCE_ID={seq_id}\n")
                f.write(f"SEQUENCE_TEMPLATE={seq_template}\n")
                
                for key, value in results.items():
                    if key == 'SEQUENCE_ID' or key == 'SEQUENCE_TEMPLATE': 
                        continue
                    
                    if isinstance(value, (list, tuple)):
                        try:
                            value = ",".join(map(str, value))
                        except TypeError:
                            value = str(value)

                    f.write(f"{key}={value}\n")
                f.write("=\n")
            except Exception as e:
                f.write(f"SEQUENCE_ID={seq_id}\n")
                f.write(f"PRIMER_ERROR={str(e)}\n")
                f.write("=\n")

if __name__ == '__main__':
    main()
