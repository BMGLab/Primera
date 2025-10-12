from dataclasses import dataclass
from typing import List, Dict

from ..Segments.sequences import FastaRecord, Sequence
from ..Utils.bedParser import BedRecord

import py2bit

@dataclass
class Primer:

    sequence : str
    tm : float = 0.0
    gc_percent : float = 0.0
    loc_start : int = 0
    loc_end : int = 0

    def __str__(self):
        return str(self.sequence)

@dataclass
class PrimerPair:

    _id : str
    forward : Primer
    reverse : Primer
    product_size : int = 0

class Primer3Input:

    def __init__(self, records: List[Dict] = None):
        
        self.records = records if records else []
    
    @staticmethod
    def calculate_primer_num(sequence_len, min_size):
        
        return int(int(sequence_len) / int(min_size)) * 2

        #TODO: Test the "coverage" approach.
    
    @classmethod
    def from_fasta(cls, fasta_record : FastaRecord, 
                   primer_count = None, 
                   min_size = 150, 
                   max_size = 300):
        
        records = []
        
        for sequence in fasta_record.sequences:
            
            if primer_count is None :
                primer_count = Primer3Input.calculate_primer_num(len(sequence),
                                                                 min_size) 
                # Giving a static number of primers as an argument will override this.

            record = {"SEQUENCE_ID" : sequence.id,
                      "SEQUENCE_TEMPLATE" : str(sequence.seq),
                      "PRIMER_PRODUCT_SIZE_RANGE" : f"{min_size}-{max_size}",
                      "PRIMER_NUM_RETURN" : primer_count}

            records.append(record)

        return cls(records)

    def to_file(self, filepath):

        with open(filepath,"w") as f:
            for record in self.records:
                for key,value in record.items():
                    f.write(f"{key}={value}\n")
                f.write("=\n")

class Primer3Output:
    def __init__(self, primer_pairs: List[PrimerPair] = None):
        self.primer_pairs = primer_pairs if primer_pairs else []

        # TODO : Maybe this can return a dict? Can be handy if we'll search something in it.

    @classmethod
    def from_matched_file(cls, filepath : str):
        
        primer_pairs = []

        with open(filepath, "r") as f:

            for line in f:
                
                _id, _forward, _reverse = line.replace("\n","").split("\t")

                forward = Primer(_forward)
                reverse = Primer(_reverse)

                primer_pairs.append(PrimerPair(_id, 
                                               forward, 
                                               reverse))

        return cls(primer_pairs)
    
    @classmethod
    def from_primer_file(cls, filepath: str):
        primer_pairs = []
        with open(filepath, "r") as f:
            data = f.read().split("=\n")
            for record in data:
                if not record.strip():
                    continue

                lines = record.strip().split("\n")
                record_dict = {}
                for line in lines:
                    key, value = line.split(",", 1) if "," in line else line.split("=", 1)
                    record_dict[key] = value

                sequence_id = record_dict.get("SEQUENCE_ID", "")

                i = 0
                while True:
                    f_key = f"PRIMER_LEFT_{i}_SEQUENCE"
                    r_key = f"PRIMER_RIGHT_{i}_SEQUENCE"
                    len_key = f"PRIMER_PAIR_{i}_PRODUCT_SIZE"


                    _id = f"{sequence_id}-{i}"

                    if f_key in record_dict and r_key in record_dict:

                        forward_primer = Primer(record_dict[f_key])
                        reverse_primer = Primer(record_dict[r_key])
                        product_size = record_dict[len_key]
                        primer_pair = PrimerPair(_id, 
                                                 forward_primer, 
                                                 reverse_primer, 
                                                 product_size)

                        # TODO: Maybe the sequence id can use the segment id somewhere?
                        primer_pairs.append(primer_pair)
                        i += 1
                    else:
                        break

        return cls(primer_pairs)

    def to_file(self, filepath):
        
        with open(filepath, "w") as f:
            
            for idx, pair in enumerate(self.primer_pairs):
                # WARNING/TODO: The use of idx here may lead to bugs. The primer id should be taken from the primer3 output file.
                
                f.write(f"{pair._id}/{idx}\t{str(pair.forward)}\t{str(pair.reverse)}\n")
