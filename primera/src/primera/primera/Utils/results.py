from ..Records.bedParser import BedRecord
from ..Primers.primers import PrimerPair, Primer3Output
from ..Segments.sequences import FastaRecord
# TODO : This code may be seperated from the primera tool. For now we will use it as it is.

import pandas as pd

class Result:

    def __init__(self, df, with_segments=False):

       self.df = df
       self.with_segments = with_segments

    @classmethod
    def from_file(cls, filepath, matched_primers_path, segments_path = ".", with_segments = True):
        
        if with_segments:
            cols = ["name","genome","segstart","segend","start","end","forward","reverse","link"]
        else:
            cols = ["name","genome","start","end","forward","reverse","link"]

        bedrecord = BedRecord.from_file(filepath)
        primersDict = {}
        newDf = []
        df = bedrecord.df
        
        primer3output = Primer3Output.from_matched_file(matched_primers_path)

        for pair in primer3output.primer_pairs:
            primersDict[pair._id] = pair

        grouped = df.groupby("sample_name")

        for _name, groupdf in grouped:

            name = _name.split("-")[0]
            chrs = ",".join(groupdf["chr"].values)
            starts = ",".join(groupdf["start"].astype(str).values)
            ends = ",".join(groupdf["end"].astype(str).values)
            
            link = Result._generate_link(primersDict[_name])

            forward = primersDict[_name].forward
            reverse = primersDict[_name].reverse
            
            if with_segments:
                # TODO : I wrote this section at 5AM on a sleepless night with no coffe. No need to say that it's terrible. Make it decent.
                segDict = {}
                segment = FastaRecord.from_file(f"{segments_path}/{name}_reversed.fa")
                
                for seq in segment.sequences:
                    segDict[seq.id.split("-")[1]] = seq.id.split("-")[2:]
 
                segstarts = ""
                segends = ""

                for genome in chrs.split(","):
                    segstarts += f"{segDict[genome][0]},"
                    segends += f"{segDict[genome][1]},"

                segstarts,segends = segstarts[:-1],segends[:-1]

                newDf.append([name, chrs, segstarts, segends, starts, ends, forward, reverse, link])
            else:
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
