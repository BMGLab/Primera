def filterCoords(filepath):

    with open(filepath, "r") as f:

        file = f.read().split("\n")[:-2]
        
        for line in file:

            line1 = line.replace("\n","").split(" ")
            
            if hash(line1[0]) + hash(line1[1]) != hash(line1[2]) + hash(line1[3]):
                
                print(line)
