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

workflow{

    filter_ch = FILTER_BLAT(params.pslFile,params.blatdb,params.filtered_chrs)
    filter_ch.view()

}
