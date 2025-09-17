params.pslFile = "not defined"
params.blatdb = "not defined"
params.filtered_chrs = "not defined"
params.outdir = workflow.projectDir

process FILTER_BLAT {

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
            
    input:
    path filtered_files_path

    output:
    path "*_primers"

    script:
    """
    primera_prepare_primers $filtered_files_path 90
    """

}

process RUN_PRIMER3 {

    
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
     
    
    
    input:
    path(allPrims)

    output:
    path "chunk_*", emit: chunk
    path "merged.txt", emit: mergedPrimers

    script:
    """
    cat ${allPrims.join(' ')} > merged.txt

    split -n l/1 merged.txt chunk_
    """

}

process RUN_ISPCR {

    
    
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

    def pp_time = new Date().format("yyyy.dd.MM_HH.mm")
 
    publishDir(
        
        path: "${params.outdir}/primera_results_${pp_time}",
        mode: "copy",
        pattern: "results.tsv" 
                )
    publishDir(

        path: "${params.outdir}/primera_results_${pp_time}",
        mode: "copy",
        pattern: "results.bed"    
                )

    input:
    path primers
    path bedFiles
    path reversedFiles
    val filteredChrs

    output:
    path "results.tsv"
    path "results.bed"

    script:
    """
    
    cat ${bedFiles.join(' ')} > out.bed

    primera_filter_bed --bedFile out.bed --primers $primers --chrs $filteredChrs
    
    primera_to_bed results.tsv results.bed

    """

}

workflow{

    filter_ch = FILTER_BLAT(params.pslFile,params.blatdb,params.filtered_chrs)

    primer_ch = PREPARE_FOR_PRIMER3(filter_ch[0]).flatten()
    
    runprimer_ch = RUN_PRIMER3(primer_ch)

    match_ch = MATCH_PRIMERS(runprimer_ch).collect()

    merge_ch = PREPARE_FOR_ISPCR(match_ch)

    ispcr_ch = RUN_ISPCR(merge_ch[0].flatten(),params.blatdb).collect()

    results_ch = WRITE_RESULTS(merge_ch[1],ispcr_ch,filter_ch[1],params.filtered_chrs)

    }

