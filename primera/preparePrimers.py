import sys
import os

def process_files(dir_path):
    files = [file for file in dir_path]

    for file_name in files:
        with open(file_name,"r") as f:
            seqList = []
            namesList = []
            
            for a,k in enumerate(f.read().split("\n")):
                if a % 2 == 0:
                    namesList.append(k.replace("\n",""))
                else:
                    seqList.append(k.replace("\n",""))
            
            namesList = namesList[:-1]
            new_output = os.path.join(f"{file_name}_primers")


            with open(new_output,"w") as f1:
                for i,j in enumerate(namesList):
                    f1.write(f"SEQUENCE_ID={j[1:]}\n")
                    f1.write(f"SEQUENCE_TEMPLATE={seqList[i]}\n")
                    f1.write("PRIMER_OUTPUT_FORMAT=0\n")
                    f1.write("PRIMER_TASK=generic\n")
                    f1.write("PRIMER_PRODUCT_SIZE_RANGE=150-250\n")
                    f1.write("PRIMER_EXPLORATORY=1\n")
                    f1.write("PRIMER_NUM_RETURN=90\n")
                    f1.write("=" + "\n")

if __name__ == "__main__":

    path = sys.argv[1:]

    process_files(path)

    
