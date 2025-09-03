params.pslFile = "not defined"
params.blatdb = "not defined"
params.filtered_chrs = "not defined"
params.outdir = workflow.projectDir

process FILTER_BLAT {

    container 'sadigngr/primera_designtest'

    publishDir(
        
        path: "${params.outdir}/clustalw_files",
        mode: "copy",
        pattern: "*_reversed.fa" 
                )
     
    input:
    path pslFile
    path blat_db
    val filtered_chrs
    
    output:
    path "*_original.fa", emit: outFile 
    path "*_reversed.fa", emit: reversed_outFile

    script:
    """
    
    primera_filter_psl -p $pslFile -c $filtered_chrs -t $blat_db --soft-filter
    
    """
    
}

process PREPARE_FOR_PRIMER3{
            
    container 'sadigngr/primera_designtest'

    input:
    path filtered_files_path

    output:
    path "*_primers"

    script:
    """
    primera_prepare_primers $filtered_files_path
    """

}

process RUN_PRIMER3 {

    container 'sadigngr/primera_designtest'
    
     publishDir(
        
        path: "${params.outdir}/primer3_output",
        mode: "copy",
                )

 
    input:
    path primerinput
    
    output:
    path "*.prim"

    script:
    """

    primer3_core < $primerinput > ${primerinput}.prim

    """

}


process MATCH_PRIMERS {

    container 'sadigngr/primera_designtest'

    input:
    path primFile

    output:
    path "matched_${primFile}"

    script:
    """
    primera_match_primers $primFile > matched_${primFile}

    """

}

process PREPARE_FOR_ISPCR {
     
    container 'sadigngr/primera_designtest'

    input:
    path(allPrims)

    output:
    path "chunk_*", emit: chunk
    path "merged.txt", emit: mergedPrimers

    script:
    """
    cat ${allPrims.join(' ')} > merged.txt

    split -n l/4 merged.txt chunk_
    """

}

process RUN_ISPCR {

    container 'sadigngr/primera_designtest'

    input:
    path primerFile
    path blat_db

    output:
    path "${primerFile}_out.bed"

    script:
    """
    isPcr $blat_db $primerFile ${primerFile}_out.bed -out=bed  
    """
}



process WRITE_RESULTS {

    container 'sadigngr/primera_designtest'

    input:
    path primers
    path bedFiles
    path reversedFiles
    val filteredChrs

    output:
    path "results.csv"

    script:
    """
    
    cat ${bedFiles.join(' ')} > out.bed

    primera_filter_bed out.bed $primers $filteredChrs $reversedFiles

    """

}

workflow{

    filter_ch = FILTER_BLAT(params.pslFile,params.blatdb,params.filtered_chrs)

    primer_ch = PREPARE_FOR_PRIMER3(filter_ch[0]).flatten()
    runprimer_ch = RUN_PRIMER3(primer_ch)

    match_ch = MATCH_PRIMERS(runprimer_ch).collect()

    merge_ch = PREPARE_FOR_ISPCR(match_ch)
    merge_ch[0].view()

    ispcr_ch = RUN_ISPCR(merge_ch[0].flatten(),params.blatdb).collect()

    results_ch = WRITE_RESULTS(merge_ch[1],ispcr_ch,filter_ch[1],params.filtered_chrs)
    results_ch.view()
}

