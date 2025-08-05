params.pslFile = "not defined"
params.blatdb = "not defined"
params.filtered_chrs = "not defined"

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
    path "*.out"
    script:
    """
    primer3_core < $primer3_input > result.out
    """
}

workflow {
    filter_ch = FILTER_BLAT(params.pslFile, params.blatdb, params.filtered_chrs)
    filter_ch.view()

    primer3_input_ch = MAKE_PRIMER3_INPUT(filter_ch)
    primer3_input_ch.view()

    primer3_ch = PRIMER3(primer3_input_ch)
    primer3_ch.view()
}


