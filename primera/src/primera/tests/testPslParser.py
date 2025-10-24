from primera.Records.pslParser import PslRecord

import time

###################

a = time.time()
#newPslRecord = PslRecord.from_file("/home/sadi/Desktop/stuff/pslFiles/output_c_100_id_95.psl")
#newPslRecord = PslRecord.from_file("/home/sadi/Desktop/stuff/pslFiles/output_with_inter.psl")
newPslRecord = PslRecord.from_file("/home/sadi/Desktop/stuff/pslFiles/newDeneme.psl")
b = time.time()
print(f"The Initial generation took {b - a} seconds.")

####################

a = time.time()
filteredRecord = newPslRecord.filter_by_target(["chr13,chr18,chr21"])
b = time.time()
print(f"Filtering with soft filter took {b - a} seconds.")

####################

a = time.time()
filtered_with_hard = newPslRecord.filter_by_target(["chr13,chr18,chr21"])
b = time.time()
print(f"Filtering with hard filter took {b - a} seconds.")

####################

a = time.time()
filled_soft = filteredRecord.fill_spaces(threshold=400)
b = time.time()
print(f"Filling the spaces in soft filtered output took {b - a} seconds.")

####################

a = time.time()
filled_hard = filtered_with_hard.fill_spaces(threshold=400)
b = time.time()
print(f"Filling the spaces in hard filtered output took {b - a} seconds.")

###################
