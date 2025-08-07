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
    path "*.fa"

    script:
    """
    python3 $baseDir/filter.py $pslFile $filtered_chrs $blat_db 
    
    mkdir -p ${params.outdir}/clustalw_files && cp *.reversed ${params.outdir}/clustalw_files
    """
    
}

process PREPARE_FOR_PRIMER3{

    input:
    path filtered_files_path

    output:
    path "*.txt"

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

    mkdir -p ${params.outdir}/primer3_output && cp ${primerinput}.prim ${params.outdir}/primer3_output
    """

}


process MATCH_PRIMERS {

    input:
    path primFile

    output:
    path "matched_${primFile}.txt"

    script:
    """
    python3 $baseDir/matchPrimers.py $primFile > matched_${primFile}.txt

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
workflow{

    filter_ch = FILTER_BLAT(params.pslFile,params.blatdb,params.filtered_chrs)

    primer_ch = PREPARE_FOR_PRIMER3(filter_ch).flatten() 
    runprimer_ch = RUN_PRIMER3(primer_ch)

    match_ch = MATCH_PRIMERS(runprimer_ch).collect()
    merge_ch = MERGE_PRIMERS(match_ch)

    merge_ch.view()

}
