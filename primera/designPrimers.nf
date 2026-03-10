params.pslFile = "not defined"
params.blatdb = "not defined"
params.filtered_chrs = "not defined"

params.outdir = workflow.projectDir
params.gfserver_port = 17779
// WARNING: The static port thing will only work for a while. 

params.fill_spaces = false
params.threshold = 18


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

    //TODO : In the script, fill-spaces should be taken from the user.
    script:
    """
    
    primera filter_psl -p $pslFile -g $filtered_chrs -t $blat_db --fill-spaces
    
    """
    
}

process PREPARE_FOR_PRIMER3{
            
    input:
    path filtered_files_path

    output:
    path "*_primers"
    
    // TODO: min size, max size etc. should be taken from the user.
    script:
    """
    primera prepare_primers -f $filtered_files_path --min-size 100 --max-size 300
    """

}

process RUN_PRIMER3 {

    
    publishDir(
        
        path: "${params.outdir}/primer3_output",
        mode: "copy",
                )

    // TODO : We need to "batch" the files for better performance. 
    input:
    path primerinput
    
    output:
    path "*.prim"

    script:
    """
    
    cat ${primerinput.join(' ')} > merged_primers

    primer3_core < merged_primers > merged_.prim

    """

}


process MATCH_PRIMERS {

    
    
    input:
    path primFile

    output:
    path "${primFile}.txt"

    script:
    """
    primera match_primers -f $primFile

    """

}

process PREPARE_FOR_ISPCR {
    //WARNING : WORK IN PROGRESS 
    input:
    path(allPrims, stageAs: "?/*")

    output:
    path "chunk_*", emit: chunk
    path "merged.txt", emit: mergedPrimers

    script:
    """
    cat ${allPrims.join(' ')} > merged.txt

    split -n l/8 merged.txt chunk_
    """

}

process RUN_ISPCR {

    // WARNING : WORK IN PROGRESS 
    
    input:
    path primerFile
    path blat_db
    val port

    output:
    path "${primerFile}_out.bed"

    script:
    """
    gfPcr host.docker.internal $port . $primerFile ${primerFile}_out.bed -out=bed  
    """
    //WARNING : Using host.docker.internal is probably unsafe. This works for now but definitely needs to be checked.
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
        pattern: "amplicons.bed"    
                )   publishDir(

        path: "${params.outdir}/primera_results_${pp_time}",
        mode: "copy",
        pattern: "segments.bed"    
                )

    input:
    path primers
    path bedFiles
    path reversedFiles
    val filteredChrs

    output:
    path "results.tsv"
    path "amplicons.bed"
    path "segments.bed"

    script:
// TODO : primera_to_bed results.tsv results.bed will be added.

//primera filter_bed --filter-locations -g $filteredChrs -b out.bed -o to_write.bed 
    """
    
    cat ${bedFiles.join(' ')} > out.bed
    
    
    primera filter_bed -g $filteredChrs -b out.bed -o to_write.bed --filter-locations -t 3 

    primera write_results -b to_write.bed -m merged.txt -o results.tsv

    primera amp_to_bed -f results.tsv -o amplicons.bed

    primera seg_to_bed -f results.tsv -o segments.bed

    """

}

workflow{

    filter_ch = FILTER_BLAT(params.pslFile, params.blatdb, params.filtered_chrs)

    primer_ch = PREPARE_FOR_PRIMER3(filter_ch[0]).flatten()
    
    primer_batches = primer_ch.buffer(size : 100, remainder : true)
    
    runprimer_ch = RUN_PRIMER3(primer_batches)

    match_ch = MATCH_PRIMERS(runprimer_ch).collect()

    merge_ch = PREPARE_FOR_ISPCR(match_ch)
    
    ispcr_ch = RUN_ISPCR(merge_ch[0].flatten(), params.blatdb, params.gfserver_port).collect()

    results_ch = WRITE_RESULTS(merge_ch[1], ispcr_ch, filter_ch[1], params.filtered_chrs)

    }

