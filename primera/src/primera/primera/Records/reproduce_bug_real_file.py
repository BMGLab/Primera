import pandas as pd
from bedParser import BedRecord
import os

def reproduce():
    filepath = "/home/sadi/Desktop/to_write.bed"
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    try:
        print(f"Loading {filepath}...")
        record = BedRecord.from_file(filepath)
        print(f"Number of records: {len(record)}")
        
        print("Filtering by location...")
        record.filter_by_location()
        print("Success!")
        
    except Exception as e:
        print(f"Caught expected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reproduce()
