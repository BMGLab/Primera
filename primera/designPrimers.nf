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
    
    mkdir -p $baseDir/clustalw_files && cp *.reversed $baseDir/clustalw_files
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
    """

}

workflow{

    primer_ch = FILTER_BLAT(params.pslFile,params.blatdb,params.filtered_chrs) | PREPARE_FOR_PRIMER3
 
    runprimer_ch = RUN_PRIMER3(primer_ch)

    runprimer_ch.view()

}
