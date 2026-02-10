import argparse
import logging
from turtle import forward
import pandas as pd
import py2bit
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Any
import sys

logging.basicConfig(level=logging.INFO, format= '%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class PrimerPair:

    id      : str
    forward : str
    reverse : str
    probe   : str = "NA"
    probe_TM: str = "NA"
    probe_GC: str = "NA"
    hits: Dict[str, List[Tuple[int, int]]] = field(default_factory=dict)
    all_chroms: List[str] = field(default_factory=list)

def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Filters isPCR results")
    parser.add_argument("-b", "--bedFile", required=True, help="Input BED file from isPCR(.bed)")
    parser.add_argument("-p", "--primers", required=True, help="Input primers file(.tsv)")
    parser.add_argument("-c", "--chrs", required=True, help="target chrs")
    parser.add_argument("-t", "--tbitFile", required=True, help="2bit file for reference genome")
    parser.add_argument("-m", "--mode", choices=["exact", "intersect", "subset"], default="exact")
    parser.add_argument("-g", "--genome", default="hg38")
    parser.add_argument("--distance_threshold", type=int, default=18)
    parser.add_argument("--allow_dup", action="store_true", help="Allow multiple hits on the same chr")
    return parser.parse_args()   

def loadPrimers(filepath : str) -> Dict[str, Dict[str, str]]:                                                       #nested dictionary

    library = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) > 3:
                    library[parts[0]] = {
                        "fwd": parts[1],
                        "rev": parts[2],
                        "probe": parts[4] if len(parts) > 4 else "NA",
                        "tm": parts[5] if len(parts) > 5 else "NA",
                        "gc": parts[6] if len(parts) > 6 else "NA"
                    }
    
    except FileNotFoundError:
        logger.error(f"Primers file not found: {filepath}")
        sys.exit(1)
    return library

def fetchGenomicSeq(tbit_path: str, hits: Dict[str, List[Tuple[int, int]]]) -> Dict[str, Dict[str, str]]:
    try:
        tb = py2bit.open(tbit_path)
        formattedSeqs = {}
        for chrom in sorted(hits.keys()):
            for start, end in hits[chrom]:
                try:
                    seq = tb.sequence(chrom, start, end)
                    formattedSeqs.append(f"{chrom}:{seq}")
                except Exception as e:
                    formattedSeqs.append(f"{chrom}:Error({str(e)})")
        tb.close()
        return " | ".join(formattedSeqs)

    except Exception as e:
        return f"2bit file error: {e}"
    

def check_chrMatch(found_chrs: List[str], target_chrs: List[str], mode: str, allow_dup: bool) -> bool:
    found_set = set(found_chrs)
    target_set = set(target_chrs)
    
    if mode == "exact":
        if allow_dup:
            return sorted(list(found_set)) == sorted(target_chrs)
        else:
            return sorted(found_chrs) == sorted(target_chrs)
    elif mode == "intersect":
        return bool(found_set & target_set)
    elif mode == "subset":
        return found_set.issubset(target_set)
    return False

def main():
    args = parseArgs()
    target_list = sorted([x.strip() for x in args.chrs.split(",")])
    primer_lib = loadPrimers(args.primers)
    pairs: Dict[str, PrimerPair] = {}

    try:

        with open(args.bedFile, "r") as f:
            for line in f:
                cols = line.strip().split()
                if len(cols) < 4: continue
                chrom, start, end, pid = cols[0], int(cols[1]), int(cols[2]), cols[3]

                if pid not in primer_lib: continue
                if pid not in pairs:
                    p = primer_lib[pid]
                    pairs[pid] = PrimerPair(pid, p["fwd"], p["rev"], p["probe"], p["tm"], p["gc"])

                pair = pairs[pid]
                if chrom not in pair.hits:
                    pair.hits[chrom] = []
                pair.hits[chrom].append((start, end))
                pair.all_chroms.append(chrom)

    except FileNotFoundError:
        logger.error(f"BED file not found: {args.bedFile}")
        sys.exit(1)


    results = []
    for pid, pair in pairs.items():
        if check_chrMatch(pair.all_chroms, target_list, args.mode, args.allow_dup):
            all_chrs, all_starts, all_ends = [], [], []
            for c in sorted(pair.hits.keys()):
                for s, e in pair.hits[c]:
                    all_chrs.append(c); all_starts.append(str(s)) ; all_ends.append(str(e))
            allTemplates = fetchGenomicSeq(args.tbitFile, pair.hits)

            results.append({
                "id"    : pair.id,
                "chrs"  : ",".join(all_chrs),
                "locs"  : ",".join(all_starts),
                "locsEnd" : ",".join(all_ends),
                "first_pos" : int(all_starts[0]),
                "forward": pair.forward,
                "reverse": pair.reverse,
                "probe_seq": pair.probe,
                "probe_TM": pair.probe_TM,
                "probe_GC": pair.probe_GC,
                "allTemplates": allTemplates,
                "ucsc_url": f"https://genome.ucsc.edu/cgi-bin/hgPcr?db={args.genome}&wp_f={pair.forward}&wp_r={pair.reverse}"
            })


    if not results:
        logger.warning("No primers passed the filtering criteria.")
        pd.DataFrame().to_csv("results.tsv", sep="\t", index=False)
        return

    
    df = pd.DataFrame(results).sort_values("first_pos")
    final_output = []
    last_hit_pos = -args.distance_threshold - 1

    for _, row in df.iterrows():
        if row['first_pos'] - last_hit_pos > args.distance_threshold:
            final_output.append(row)
            last_hit_pos = row['first_pos']

    final_df = pd.DataFrame(final_output).drop(columns=['first_pos'])
    final_df.to_csv("results.tsv", sep="\t", index=False)
    logger.info(f"Process completed. {len(final_df)} primer pairs saved to results.tsv.")

if __name__ == "__main__":
    main()
