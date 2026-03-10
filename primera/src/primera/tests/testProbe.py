from primera.Primers.primers import Primer3ProbeInput, Primer3ProbeOutput
from primera.Records.bedParser import BedRecord

#newBed = BedRecord.from_file("out.bed")
newBed = BedRecord.from_file("~/Desktop/to_write.bed")
print(len(newBed.as_df))
#filteredBed = newBed.filter_by_target(["chr13","chr18","chr21"])
filteredBed = newBed.filter_by_target(["chr7","chr14"]).filter_by_location()
print(len(filteredBed.as_df))
newprobes = Primer3ProbeInput.from_bed_record(filteredBed,"/home/sadi/Desktop/stuff/hg38.2bit",65.0,67.0,69.0)

newprobes.to_file("selam.txt")
probeout = Primer3ProbeOutput.from_primer_file("./selam_77_.txt.primers")


for i in probeout.probe_groups:
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(i)
    for j in probeout.probe_groups[i]:
        print(f"\nCHROMOSOME : {j}")
        print(f"\nSEQUENCE : {probeout.probe_groups[i][j].seq}")
        print(f"\nPROBES : {probeout.probe_groups[i][j].probes}")

