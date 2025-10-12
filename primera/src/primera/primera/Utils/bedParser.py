import pandas as pd
import sys

from .Record import Df_Like_Record 

class BedRecord(Df_Like_Record):

    def __init__(self,df):

        super().__init__(df)

    @classmethod
    def from_file(cls, filepath):
        
        _DEFAULT_COLS = ["chr", "start", "end", 
                "sample_name", "score", "strand"]

        try:
            df = pd.read_csv(filepath, 
                             sep='\t', 
                             header=None, 
                             names=_DEFAULT_COLS, 
                             skiprows=0) 

        except FileNotFoundError:
            raise FileNotFoundError(f"BED file not found at: {filepath}")
        except Exception as e:
            raise ValueError(f"Failed to parse BED file: {e}")
        
        return cls(df)

    def filter_by_target(self, allowed_chr_list):
        
        _dfList = []
        allowed_chrs_sorted = sorted(allowed_chr_list)
        
        grouped = self.df.groupby("sample_name")

        for _, group_df in grouped:
        
            chrs = sorted(list(group_df["chr"]))
            if chrs == allowed_chrs_sorted:

                _dfList.extend(group_df.index)

        if not _dfList:

            return BedRecord(pd.DataFrame(columns = self.df.columns))

        return BedRecord(self.df.loc[_dfList].copy())

    def filter_by_location(self, threshold = 18):
        
        # TODO : This code looks sloppy. Make it prettier.

        _df = self.df.copy()

        _df["start"] = pd.to_numeric(_df["start"])

        _df = _df.sort_values(["chr", "start"])

        _df["drop_flag"] = _df.groupby("chr")["start"].diff().abs().fillna(threshold + 1) < threshold
        # WARNING : Is the fillna() method safe from bugs? 

        to_drop = (_df.groupby("sample_name")["drop_flag"]
                   .transform(lambda x : x.all()))

        _df = _df[~to_drop].copy()

        self.df = _df.drop("drop_flag", axis=1)

        return self
