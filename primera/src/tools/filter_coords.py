import sys

def main():
    with open(sys.argv[1],"r") as f:  
        file = f.read().split("\n")[:-1]
        
        for line in file:

            line1 = line.replace("\n","").split(" ")
            
            if hash(line1[0]) + hash(line1[1]) != hash(line1[2]) + hash(line1[3]):
                
                print(line)
