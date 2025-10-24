from ..Records.bedParser import BedRecord
from ..Primers.primers import PrimerPair, Primer3Output

import pandas as pd

class Result:

    def __init__(self, df):

       self.df = df 

    @classmethod
    def from_file(cls, filepath, matched_primers_path): 
        cols = ["name","genome","start","end","forward","reverse","link"]
        
        bedrecord = BedRecord.from_file(filepath)
        primersDict = {}
        newDf = []
        df = bedrecord.df
        
        primer3output = Primer3Output.from_matched_file(matched_primers_path)

        for pair in primer3output.primer_pairs:
            primersDict[pair._id] = pair

        grouped = df.groupby("sample_name")

        for name, groupdf in grouped:

            chrs = ",".join(groupdf["chr"].values)
            starts = ",".join(groupdf["start"].astype(str).values)
            ends = ",".join(groupdf["end"].astype(str).values)
            
            link = Result._generate_link(primersDict[name])

            forward = primersDict[name].forward
            reverse = primersDict[name].reverse

            newDf.append([name, chrs, starts, ends, forward, reverse, link])

        new_df = pd.DataFrame(newDf, columns=cols)
        return cls(new_df)
    
    @staticmethod
    def _generate_link(pair : PrimerPair):

        template_url = "https://genome.ucsc.edu/cgi-bin/hgpcr?hgsid=2900325362_8e48bzufkdycxxspnallnmzhkyga&org=human&db=hg38&wp_target=genome&wp_f={f}&wp_r={r}&submit=submit&wp_size=300&wp_perfect=15&wp_good=15&boolshad.wp_flipreverse=0&wp_append=on&boolshad.wp_append=0"

        return template_url.format(f=pair.forward, r=pair.reverse)

    def to_file(self, filepath):

        self.df.to_csv(filepath, 
                       sep="\t", 
                       header=True, 
                       index=False)
