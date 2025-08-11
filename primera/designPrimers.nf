params.pslFile        = "not defined"
params.blatdb         = "not defined"
params.filtered_chrs  = "not defined"

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
    """
}

process MAKE_PRIMER3_INPUT {
    input:
    path seq
    output:
    path "primer3_input.txt"
    script:
    """
    python3 $baseDir/prim_input.py $seq primer3_input.txt
    """
}

process PRIMER3 {
    input:
    path primer3_input
    output:
    path "result.out"
    script:
    """
    primer3_core < $primer3_input > result.out
    """
}

process EXTRACT_PRIMERS {
    input:
    path primer3_output
    output:
    path "primer_pairs.txt"
    script:
    """
    python3 $baseDir/extract_primers.py primer_pairs.txt $primer3_output
    """
}

process ISPCR {
    input:
    path primer_pairs
    path blat_db
    output:
    path "output.bed"
    script:
    """
    isPcr $blat_db $primer_pairs output.bed -out=bed
    """
}

process FILTER_BED {
    input:
    path bedfile
    path primer_pairs
    output:
    path "primer_result.txt"
    script:
    """
    python3 $baseDir/filter_bed.py $bedfile $primer_pairs primer_result.txt
    """
}

process FILTER_FINAL {
    input:
    path primer_result
    val filtered_chrs
    output:
    path "primer_result_filtered.txt"
    publishDir "${baseDir}/${filtered_chrs}", mode: 'copy'
    script:
    """
    python3 $baseDir/filter_final.py $primer_result "$filtered_chrs" primer_result_filtered.txt
    """
}

process ADD_URL {
    input:
    path primer_result_filtered
    output:
    path "primers_with_urls.xlsx"
    publishDir "${baseDir}/${params.filtered_chrs}", mode: 'copy'
    script:
    """
    python3 $baseDir/url.py $primer_result_filtered primers_with_urls.xlsx
    """
}

workflow {
    filter_ch         = FILTER_BLAT(params.pslFile, params.blatdb, params.filtered_chrs)
    primer3_input_ch  = MAKE_PRIMER3_INPUT(filter_ch)
    
    println "The Results:"
    
    primer3_ch        = PRIMER3(primer3_input_ch)
    primer3_ch.view()

    primer_pairs_ch   = EXTRACT_PRIMERS(primer3_ch)
    primer_pairs_ch.view()

    ispcr_ch          = ISPCR(primer_pairs_ch, params.blatdb)
    ispcr_ch.view()

    filter_bed_ch     = FILTER_BED(ispcr_ch, primer_pairs_ch)
    filter_bed_ch.view()

    filter_final_ch   = FILTER_FINAL(filter_bed_ch, params.filtered_chrs)
    filter_final_ch.view()

    url_append_ch     = ADD_URL(filter_final_ch)
    url_append_ch.view()
}
