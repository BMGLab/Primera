nextflow.enable.dsl=2

params.psl   = "not defined"
params.fasta = "not defined"
params.chrs  = "not defined"

log.info"""\

            P R I M E R A

"""
process filter_psl {
    input:
    path psl_file
    val chrs

    output:
    path "selected_ids.txt"

    script:
    """
    python3 $baseDir/filter_nf.py $psl_file '$chrs' selected_ids.txt
    """
}

process extract_seqs {
    input:
    path fasta_file
    path id_file

    output:
    path "selected_seqs.fa"

    script:
    """
    python3 $baseDir/extract_nf.py $fasta_file $id_file selected_seqs.fa
    """
}

workflow {
    psl_ch = Channel.fromPath(params.psl)
    fasta_ch = Channel.fromPath(params.fasta)
    chrs_val = params.chrs

    filtered_ids = filter_psl(psl_ch, chrs_val)
    extract_seqs(fasta_ch, filtered_ids)
    fasta_ch.view()

    println "The results can be found on: "
    filtered_ids.view()
}
