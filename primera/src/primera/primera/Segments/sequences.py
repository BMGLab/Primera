from typing import List
from Bio.Seq import Seq
import warnings

class Sequence:
    def __init__(self, id: str, seq: str, description: str = ""):
        self.id = id
        self.seq = Seq(seq)
        self.description = description

    def reverse_complement(self):
        return Sequence(self.id, str(self.seq.reverse_complement()), self.description)

    def __len__(self):

        return len(self.seq)

    def __str__(self):

        if self.seq:

            return str(self.seq)

        else:

            raise Exception("The sequence is empty!")
            # TODO : This will be replaced by a real thing. 
            

class FastaRecord:
    def __init__(self, name = None, sequences: List[Sequence] = None):
        self.sequences = sequences if sequences else []
        self.name = name
    
    @property
    def get_name(self):
        
        if self.name is None:
            warnings.warn("This FastaRecord object does not have a name.")
        
        return self.name

    @classmethod
    def from_file(cls, filepath: str):
        sequences = []
        with open(filepath, "r") as f:
            sequence_id = None
            sequence_description = ""
            sequence_str = ""
            for line in f:
                if line.startswith(">"):
                    
                    if sequence_id:
                        sequences.append(Sequence(sequence_id, sequence_str, sequence_description))

                    parts = line[1:].strip().split(maxsplit=1)
                    sequence_id = parts[0]
                    sequence_description = parts[1] if len(parts) > 1 else ""
                    sequence_str = ""
                else:
                    sequence_str += line.strip()
            
            if sequence_id:
                sequences.append(Sequence(sequence_id, sequence_str, sequence_description))
        
        return cls(sequences=sequences)

    def to_file(self, filepath: str):
        with open(filepath, "w") as f:
            for seq in self.sequences:
                f.write(f">{seq.id} {seq.description}\n{seq.seq}\n")

    def add_sequence(self, sequence : Sequence):

        self.sequences.append(sequence)
