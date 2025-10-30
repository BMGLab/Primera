from .Segments.sequences import Sequence, FastaRecord

from .Primers.primers import Primer3Input, Primer3Output

from .Records.pslParser import PslRecord
from .Records.bedParser import BedRecord

from .Utils.results import Result
from .Utils.result_to_bed import writeToBed
from .Utils.filter_coords import filterCoords

import argparse

def filter_psl(psl, genomes, tbitFile, threshold, fillspaces = False):
 
    psl_record = PslRecord.from_file(psl)

    filtered_record = psl_record.filter_by_target(genomes)

    if fillspaces:
        filtered_record.fill_spaces(threshold)

    segments = filtered_record.extract_groups(tbitFile, reverse_complement=False)

    segments_reversed = filtered_record.extract_groups(tbitFile, reverse_complement=True)
    

    for seg in segments:

        seg.to_file(f"{seg.name}_original.fa")

    for seg_r in segments_reversed:

        seg_r.to_file(f"{seg_r.name}_reversed.fa")


def filter_bed(bed, genomes, outfile, threshold, filterlocation=True):
    
    bed_record = BedRecord.from_file(bed)

    filtered_bed = bed_record.filter_by_target(genomes)

    if filterlocation:

        filtered_bed.filter_by_location(int(threshold))

    filtered_bed.to_file(outfile)

def prepare_primers(segmentFiles, minSize, maxSize, primerCount):
    
    for seg in segmentFiles:
        
        record = FastaRecord.from_file(seg)
        newInput = Primer3Input.from_fasta(record, 
                                           primerCount, 
                                           minSize, 
                                           maxSize)

        newInput.to_file(f"{seg}_primers")

def match_primers(files, matched=False):

    for p3file in files:
        
        if matched:
            newOutput = Primer3Output.from_matched_file(p3file)
        else:
            newOutput = Primer3Output.from_primer_file(p3file)

        newOutput.to_file(f"{p3file}.txt")

        # TODO : Add default out file name.

def write_results(bedfile, matchedfile, outfile):
    
    newResult = Result.from_file(bedfile,matchedfile)
    newResult.to_file(outfile)

def to_bed(filepath, outfile):
    writeToBed(filepath, outfile)

def main():

    """
    The main function. Holds the parsers and runs all of the necessary functions. The default
    values like threshold for filtering nearby primers etc. are also stored in the ArgumentParser object.
    """
   
    # Default values for some prepare_primers args.
    _DEFAULT_MIN_AMPLICON_SIZE = 150
    _DEFAULT_MAX_AMPLICON_SIZE = 300
    _DEFAULT_NUM_PRIMERS = 0
    
    # Default values for some filter_bed args.
    _DEFAULT_FILTERING_THRESHOLD = 18

    # Default values for some filter_psl args. 
    _DEFAULT_FILL_SPACES_THRESHOLD = 400
    
    parser = argparse.ArgumentParser(description="Primera command-line tool")
    
    subparsers = parser.add_subparsers(dest="command")

    ############# primera filter_psl ###################################################################
    filter_parser = subparsers.add_parser("filter_psl", help="Filter PSL files and extract segments as groups.")
    
    filter_parser.add_argument("-p","--psl", required=True, help="Path to the PSL file.")
    filter_parser.add_argument("-g","--genomes", required=True ,help="Comma-seperated list of target genomes.")
    filter_parser.add_argument("-t","--tbitFile", required=True, help="Path to the .2bit file.")
    filter_parser.add_argument("-f", "--fill-spaces", action="store_true", help="Merge nearby segments")
    filter_parser.add_argument ("--threshold", default=_DEFAULT_FILL_SPACES_THRESHOLD, help="The threshold for fill_spaces.")
    #TODO : Change this help str.
    
    ############# primera filter_bed ##############################################################
    filter_bed_parser = subparsers.add_parser("filter_bed", help="Filter BED files and extract primers.")
   
    filter_bed_parser.add_argument("-g", "--genomes", required=True, help="Comma-seperated list of target genomes")
    filter_bed_parser.add_argument("-b", "--bedfile", required=True, help="Path to the BED file.")
    filter_bed_parser.add_argument("-f", "--filter-locations", action="store_true", help="Filter nearby primer pairs for all of the genomes provided.")
    filter_bed_parser.add_argument("-t","--threshold",default=_DEFAULT_FILTERING_THRESHOLD,help="""The minimum space allowed between two generated primers. 
                                   The rest will be filtered out. Default=18""")
    filter_bed_parser.add_argument("-o", "--outfile", required=True, help="The output file path.")

    ############### primera prepare_primers ############################################################
   
   # WARNING/TODO : The file management should be done by Nextflow only. We're using a temporary solution.

    # Right now, the prepare_primers tool does all of the file management. It takes all of the segment files
    # and generate all of the primer3 input files. The tool should be responsible from only generating a single
    # primer3 input file from a segment file. Nextflow should be handling how segment files or primer3 input
    # files are stored and transferred throughout runtime.
    
    prepare_primers_parser = subparsers.add_parser("prepare_primers", help="Prepare Primer3 Input with desired attributes.")
    
    prepare_primers_parser.add_argument("-f", "--files", nargs="+", required=True, help="Path to the segment files.")
    prepare_primers_parser.add_argument("--num-primers", default=_DEFAULT_NUM_PRIMERS, help="""Static primer count for all of the segments. 
                                        If not provided, the tool will try to calculate a 'sufficient' number of primers to generate.""")
    prepare_primers_parser.add_argument("--min-size", default=_DEFAULT_MIN_AMPLICON_SIZE, help="Minimum amplicon size. Default=150")
    prepare_primers_parser.add_argument("--max-size", default=_DEFAULT_MAX_AMPLICON_SIZE, help="Maximum amplicon size. Default=300")

    ############### primera match_primers #################################################################
    
    match_primers_parser= subparsers.add_parser("match_primers", help="Convert Primer3 output to isPcr input files.")
    
    match_primers_parser.add_argument("-f","--files", nargs="+", required=True, help="File path for primer3 output files.")
    match_primers_parser.add_argument("--from-matched", action="store_true", help="Use if you want to parse a matched file.")

 ################## primera write_results #####################################################################
    
    write_results_parser = subparsers.add_parser("write_results", help="Write results.")

    write_results_parser.add_argument("-b","--bedfile", required=True, help="Path to the BED file.")
    write_results_parser.add_argument("-m","--matchedfile", required=True, help="Path to the matched file generated by primera match_primers.")
    write_results_parser.add_argument("-o", "--outfile", required=True, help="Path to the output file.")
    ################# primera to_bed ###########################################################################

    to_bed_parser = subparsers.add_parser("to_bed", help= "Return results in a BED format.")

    to_bed_parser.add_argument("-f","--file", required=True, help="Path to the result file.")
    to_bed_parser.add_argument("-o","--outfile", required=True, help="Output file name.")
    ############## primera filter_coords #####################################################################

    filter_coords_parser = subparsers.add_parser("filter_coords", help="Filter NUCMER's .coords file.")
    
    filter_coords_parser.add_argument("-f", "--file", help="The path to the .coords file.")
    

    args = parser.parse_args()
    
    match args.command:

        case "filter_psl":

            genomes = [c.strip() for c in args.genomes.split(",")]

            filter_psl(args.psl, genomes, args.tbitFile, args.threshold,args.fill_spaces)

        case "filter_bed":

            genomes = [c.strip() for c in args.genomes.split(",")]

            filter_bed(args.bedfile, genomes, args.outfile, args.threshold, args.filter_locations)

            #TODO : If threshold is not provided, a warning message can be given.

        case "prepare_primers":

            prepare_primers(args.files, args.min_size, args.max_size, args.num_primers)

        case "match_primers":

            match_primers(args.files, args.from_matched)

        case "write_results":

            write_results(args.bedfile, args.matchedfile, args.outfile)
        
        case "to_bed":
            
            to_bed(args.file, args.outfile)

        case "filter_coords":
            
            filterCoords(args.file)
