import pandas as pd
from typing import List
import py2bit

from ..Segments.sequences import Sequence, FastaRecord
from .Record import Df_Like_Record

class PslRecord(Df_Like_Record):
    
    def __init__(self, df):
        
        """Users should typically use the PslRecord.from_file() classmethod."""
        
        super().__init__(df)
    
    @classmethod
    def from_file(cls, filepath):

        # This must not be changed.
        _DEFAULT_COLS = [
                "match", "mis-match", "rep-match", "N's", "Q gap count", "Q gap bases",
                "T gap count", "T gap bases", "strand",
                "Q name", "Q size", "Q start", "Q end",
                "T name", "T size", "T start", "T end",
                "block count", "blockSizes", "qStarts", "tStarts"]
        
        try:
            df = pd.read_csv(filepath, 
                             sep='\t', 
                             header=None, 
                             names=_DEFAULT_COLS, 
                             skiprows=4) 

        except FileNotFoundError:
            raise FileNotFoundError(f"PSL file not found at: {filepath}")
        except Exception as e:
            raise ValueError(f"Failed to parse PSL file: {e}")

        #df = df[~df["T name"].str.contains("_", na=False)]
        # Get rid off the chr_alt or that kinda stuff that are present in the file.
        # TODO: This approach is not safe. Find a better way to filter out those things.
        # TODO: Also the static name approach should be reconsidered.

        df = df.sort_values("Q name")
        #TODO: I don't know why i sorted the values. Need to check this later.
       
        return cls(df)


    def filter_by_target(self, allowed_chr_list: List, hard_filter=False):
        # WARNING : The filter condition (like chromosomes) MUST be passed as a list. 
        # Gonna define it in the main function. 
         
        _df = pd.DataFrame(columns=self.df.columns.tolist())
        # TODO: Is this thing used? Maybe we can delete this.
            
        chrs_sorted = sorted(allowed_chr_list)

        grouped = self.df.groupby("Q name")
         
        filtered_dfList = []

        for _, group_df in grouped:

            if hard_filter:
                t_names = sorted(list(group_df["T name"]))

                if t_names == chrs_sorted:
                    filtered_dfList.extend(group_df.index)

            else:
                t_names = set(group_df["T name"].unique())

                if t_names == set(allowed_chr_list):

                    filtered_dfList.extend(group_df.index)
                            
            if len(t_names) == 1 and len(allowed_chr_list) != 1:
                continue
        
        if not filtered_dfList:
            return PslRecord(pd.DataFrame(columns=self.df.columns))
        
        return PslRecord(self.df.loc[filtered_dfList].copy())
       
    def fill_spaces(self, 
                threshold=400,
                namesCol = "T name", 
                startCol="T start", 
                endCol = "T end"):


        #TODO: This approach possibly creates duplicate segments. Need to check if it does and fix it.

        """
        Merges adjacent segments that are within the specified threshold.

        This method modifies the record in-place AND returns the modified
        instance to allow for method chaining.
        """

        if self.df.empty:
            return self
        
        df_copy = self.df.copy()
        df_copy["init_idx"] = df_copy.index.values

        grouped = df_copy.groupby(namesCol)

        for _, groupdf in grouped:
            
            groupdf.sort_values(by=startCol, ascending=True, inplace=True)
            
            dfList = []
            idxList = []
            cur_start = None
            cur_end = None 

            for _, row in groupdf.iterrows():
               
                start, end = row[startCol], row[endCol]
                
                idx = row["init_idx"]
                
                if cur_start is None:
                    cur_start, cur_end = start, end
 
                elif start - cur_end <= threshold:

                    idxList.append(idx)
                    cur_end = max(cur_end, end)

                else:

                    dfList.append([idxList, cur_start, cur_end]) 
                    idxList = []
                    cur_start, cur_end = start, end

            if cur_start is not None :
                # This is For The Last Block 
                dfList.append([idxList, cur_start, cur_end])

            for idxList, start, end in dfList:
                for idx in idxList:
                    self.df.loc[idx, "T start"] = start
                    self.df.loc[idx, "T end"] = end
        

        return self
 
    def extract_groups(self, two_bit_filepath, reverse_complement: bool):
        """
        Extracts DNA sequences for each record, oriented according to the strand,
        and returns them as a single FastaRecord object.
        """

        #TODO: Splitting the grouping part and the actual FastaRecord generation part may be helpful in the future.
        fastaRecords = []

        try:
            self.tbitFile = py2bit.open(two_bit_filepath)

        except FileNotFoundError:
            raise FileNotFoundError(f"2bit file not found at: {two_bit_filepath}")


        for _, groupdf in self.df.groupby("Q name"):

            fasta_record = FastaRecord()

            for _, row in groupdf.iterrows():
                try:
                    name = row["T name"]
                    start = int(row["T start"])
                    end = int(row["T end"])

                    sequence_str = self.tbitFile.sequence(str(row["T name"]), 
                                                     start, 
                                                     end)

                    seq_id = f"{name}-{start}-{end}"
                    # TODO : Check "-" character's effect.

                    seq = Sequence(seq_id, sequence_str)

                    if reverse_complement and row["strand"] == "-":

                        fasta_record.add_sequence(seq.reverse_complement())

                    else:

                        fasta_record.add_sequence(seq)
                    
                except Exception as e:
                    print(f"Warning: Could not process record {row['Q name']}: {e}")
             
            fastaRecords.append(fasta_record)
        return fastaRecords
