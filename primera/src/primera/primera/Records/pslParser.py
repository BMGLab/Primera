import pandas as pd
from typing import List
import py2bit
import warnings

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
                "Q name", "T name", "T start", "T end", "strand"]

        try:
            df = pd.read_csv(filepath, 
                             sep='\t', 
                             header=None, 
                             names=_DEFAULT_COLS, 
                             skiprows=5,
                             engine="pyarrow",
                             )

        except FileNotFoundError:
            raise FileNotFoundError(f"PSL file not found at: {filepath}")
        except Exception as e:
            raise ValueError(f"Failed to parse PSL file: {e}")

        #df = df[~df["T name"].str.contains("_", na=False)]
        # Get rid off the chr_alt or that kinda stuff that are present in the file.
        # TODO: This approach is not safe. Find a better way to filter out those things.
        # TODO: Also the static name approach should be reconsidered.

        #df = df.sort_values("Q name")
        #TODO: I don't know why i sorted the values. Need to check this later.
       
        return cls(df)


    def filter_by_target(self, allowed_chr_list: List):

        if self.df.empty:
            return PslRecord(pd.DataFrame(columns=self.df.columns))

        allowed_set = set(allowed_chr_list)
        
        # Find all Q names that contain at least one T name not in the allowed list.
        invalid_q_names = self.df[~self.df['T name'].isin(allowed_set)]['Q name'].unique()
        
        # Filter the DataFrame to keep only Q names that do not have any invalid T names.
        candidates = self.df[~self.df['Q name'].isin(invalid_q_names)]
        
        # Among the candidates, find the Q names that have the correct number of unique T names.
        # This ensures that they have all the T names from the allowed list.
        if not candidates.empty:
            q_name_counts = candidates.groupby('Q name')['T name'].nunique()
            valid_q_names = q_name_counts[q_name_counts == len(allowed_set)].index
        else:
            valid_q_names = []

        # Filter the original DataFrame to get the final result.
        result_df = self.df[self.df['Q name'].isin(valid_q_names)]
        
        if result_df.empty:
            return PslRecord(pd.DataFrame(columns=self.df.columns))
            
        return PslRecord(result_df.copy())
       
    def fill_spaces(self, 
                threshold,
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
 
                elif start - cur_end<= int(threshold):

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
        AND returns them as a single FastaRecord object.
        """

        #TODO: Splitting the grouping part and the actual FastaRecord generation part may be helpful in the future.
        
        # WARNING : This function is written as if the PslRecord object will never 
        # change dynamically along the runtime of it. If the object is changed somehow while 
        # this is running, serious bugs can occur.

        fastaRecords = []

        try:
            self.tbitFile = py2bit.open(two_bit_filepath)

        except FileNotFoundError:
            raise FileNotFoundError(f"2bit file not found at: {two_bit_filepath}")

        seg_count = 0

        for _, groupdf in self.df.groupby("Q name"):
            
            _name = f"seg_{seg_count}"
            fasta_record = FastaRecord(name=_name)

            for _, row in groupdf.iterrows():
                try:

                    start = int(row["T start"])
                    end = int(row["T end"])

                    name = f"seg_{seg_count}-{row["T name"]}-{start}-{end}"
                    sequence_str = self.tbitFile.sequence(str(row["T name"]), 
                                                     start, 
                                                     end)

                    seq_id = f"{name}"
                    # TODO : Check "-" character's effect.

                    seq = Sequence(seq_id, sequence_str)

                    if reverse_complement and row["strand"] == "-":

                        fasta_record.add_sequence(seq.reverse_complement())

                    else:

                        fasta_record.add_sequence(seq)
                    
                except Exception as e:
                    warnings.warn(f"Warning: Could not process record {row['Q name']}: {e}")

            seg_count += 1
             
            fastaRecords.append(fasta_record)

        return fastaRecords
