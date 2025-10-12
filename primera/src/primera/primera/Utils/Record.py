import pandas as pd

from abc import ABC, abstractmethod

class Df_Like_Record(ABC): 

    def __init__(self, df) -> None:

        self.df = df
        
    @property
    def as_df(self) -> pd.DataFrame:

        return self.df
    
    def __len__(self) -> int:
        return len(self.df.index)

    
    @classmethod
    @abstractmethod
    def from_file(cls, filepath):
        raise NotImplementedError
 
    def to_file(self, filepath) -> None:

        self.df.to_csv(filepath, sep="\t", index=False, header=False)
