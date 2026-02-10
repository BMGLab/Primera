params.pslFile          = "not defined"
params.blatdb           = "not defined"
params.filtered_chrs    = "not defined"
params.filter_mode      = "not defined"
params.mode             = "not defined"
params.outdir           = workflow.projectDir
params.primer_config    = "${workflow.projectDir}/primerSettings.json"

params.scripts_dir = "$projectDir/../src/tools"
params.primer_chunk_size = 500

process FILTER_BLAT {
    cpus 2 
    publishDir "${params.outdir}/clustalw_files", mode: "copy", pattern: "*_reversed.fa"
     
    input:
    path pslFile
    path blat_db
    val filtered_chrs
    val filter_mode
    path script_file
    
    output:
    path "*_original.fa", emit: outFile 
    path "*_reversed.fa", emit: reversed_outFile

    script:
    """
    python3 $script_file \
            -p $pslFile \
            -c $filtered_chrs \
            -t $blat_db \
            --mode $filter_mode 
    """
}

process RUN_PRIMER3 {
    cpus 2
    publishDir "${params.outdir}/primer3_output", mode: "copy"

    input:
    path primerinput
    path config_file
    path script_file
    
    output:
    path "*.prim"

    script:
    """
    python3 $script_file \
            $primerinput \
            --config $config_file
    """
}

process MATCH_PRIMERS {
    cpus 2
    input:
    path primFile
    path script_file

    output:
    path "matched_${primFile}"

    script:
    """
    python3 $script_file \
            $primFile > matched_${primFile}
    """
}

process PREPARE_FOR_ISPCR {
    cpus 2
    input:
    path(allPrims)

    output:
    path "chunk_*", emit: chunk
    path "merged.txt", emit: mergedPrimers

    script:
    """
    cat ${allPrims.join(' ')} > merged.txt
    split -n l/16 merged.txt chunk_
    """
}

process RUN_ISPCR {
    cpus 2
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

process FILTER_SUCCESSFUL_PRIMERS {
    cpus 2

    input:
    path primers_to_filter
    path bedFiles
    val filteredChrs
    val mode
    path blat_db
    path script_file

    output:
    path "successful_primers.tsv"

    script:
    """
    cat ${bedFiles.join(' ')} > out.bed

    python3 $script_file \
        --bedFile out.bed \
        --primers $primers_to_filter \
        --chrs $filteredChrs \
        --mode $mode \
        --tbitfile $blat_db \
        --distance_threshold 18 \
        --allow_dup true
    
    mv results.tsv successful_primers.tsv
    """
}

process WRITE_RESULTS {
    cpus 2
    def pp_time = new Date().format("yyyy.dd.MM_HH.mm")
    publishDir "${params.outdir}/primera_results_${pp_time}", mode: "copy"

    input:
    path final_results_tsv
    path script_file

    output:
    path "results.tsv"
    path "results.bed"

    script:
    """
    cp $final_results_tsv results.tsv
    python3 ${params.scripts_dir}/writeToBED.py results.tsv results.bed

    """
}

workflow {

    def filter_script     = file("${params.scripts_dir}/filter.py")
    def primer3_script    = file("${params.scripts_dir}/runPrimer3.py")
    def match_script      = file("${params.scripts_dir}/matchPrimers.py")
    def filter_bed_script = file("${params.scripts_dir}/filterBED.py")
    def write_bed_script  = file("${params.scripts_dir}/writeToBED.py")


    def config_ch = file(params.primer_config)

    filter_ch = FILTER_BLAT(params.pslFile, params.blatdb, params.filtered_chrs, params.filter_mode, filter_script)
    
    primer3_input_ch = filter_ch.reversed_outFile.flatten().splitFasta(by: params.primer_chunk_size, file: true)
    config_ch = file(params.primer_config)

    runprimer_ch = RUN_PRIMER3(primer3_input_ch, config_ch, primer3_script)
    match_ch = MATCH_PRIMERS(runprimer_ch, match_script).collect()
    merge_ch = PREPARE_FOR_ISPCR(match_ch)
    ispcr_ch = RUN_ISPCR(merge_ch.chunk.flatten(), params.blatdb).collect()

    successful_primers_ch = FILTER_SUCCESSFUL_PRIMERS(
                                merge_ch.mergedPrimers,
                                ispcr_ch,
                                params.filtered_chrs,
                                params.mode,
                                params.blatdb,
                                filter_bed_script
                            )

    WRITE_RESULTS(successful_primers_ch, write_bed_script)
}