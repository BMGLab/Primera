params.pslFile = "not defined"
params.blatdb = "not defined"
params.filtered_chrs = "not defined"
params.outdir = workflow.projectDir

process FILTER_BLAT {

    input:
    path pslFile
    path blat_db
    val filtered_chrs
    
    output:
    path "*_original.fa", emit: outFile 
    path "*_reversed.fa", emit: reversed_outFile

    script:
    """
    python3 $baseDir/filter.py $pslFile $filtered_chrs $blat_db 
    
    mkdir -p ${params.outdir}/clustalw_files && cp *_reversed.fa ${params.outdir}/clustalw_files
    """
    
}

process PREPARE_FOR_PRIMER3{

    input:
    path filtered_files_path

    output:
    path "*_primers"

    script:
    """
    python3 $baseDir/preparePrimers.py $filtered_files_path
    """

}

process RUN_PRIMER3 {


    input:
    path primerinput
    
    output:
    path "*.prim"

    script:
    """

    primer3_core < $primerinput > ${primerinput}.prim

    mkdir -p ${params.outdir}/primer3_output && cp  ${primerinput}.prim ${params.outdir}/primer3_output
    """

}


process MATCH_PRIMERS {

    input:
    path primFile

    output:
    path "matched_${primFile}"

    script:
    """
    python3 $baseDir/matchPrimers.py $primFile > matched_${primFile}

    """

}

process MERGE_PRIMERS {

    input:
    path(allPrims)

    output:
    path "merged.txt"

    script:
    """
    cat ${allPrims.join(' ')} > merged.txt
    """

}

process RUN_ISPCR {

    input:
    path mergedFile
    path blat_db

    output:
    path "_output.bed"

    script:
    """
    isPcr $blat_db $mergedFile _output.bed -out=bed  
    """
}

process WRITE_RESULTS {

    input:
    path primers
    path bedFile
    path reversedFiles
    val filteredChrs

    output:
    path "results.csv"

    script:
    """
    
    python3 $baseDir/filter_bed.py $bedFile $primers o.bed

    python3 $baseDir/filter_final.py o.bed $filteredChrs output.csv
    
    python3 $baseDir/lastFilter.py output.csv

    python3 $baseDir/url.py last.csv results.csv 
    """

}


/*


    ""python3 $baseDir/deneme1.py $bedFile $primers > o.bed

awk '\$5 == 1000 {count[\$4]++; lines[\$4] = lines[\$4] \$0 ORS}
    END {
     for (id in count) {
         if (count[id] == 2) {
             printf "%s", lines[id]
         }
     }
    }' _output.bed > output.bed 
*/

workflow{

    filter_ch = FILTER_BLAT(params.pslFile,params.blatdb,params.filtered_chrs)

    primer_ch = PREPARE_FOR_PRIMER3(filter_ch[0]).flatten()
    runprimer_ch = RUN_PRIMER3(primer_ch)

    match_ch = MATCH_PRIMERS(runprimer_ch).collect()
    merge_ch = MERGE_PRIMERS(match_ch)

    ispcr_ch = RUN_ISPCR(merge_ch,params.blatdb)

    results_ch = WRITE_RESULTS(merge_ch,ispcr_ch,filter_ch[1],params.filtered_chrs)
    results_ch.view()
}
