params.filePath = "not defined"
params.blatdb = "not defined" 

                                                                   


log.info """\
                              
                                                                                            
        ▀███▀▀▀██▄▀███▀▀▀██▄ ▀████▀████▄     ▄███▀███▀▀▀███▀███▀▀▀██▄       ██      
          ██   ▀██▄ ██   ▀██▄  ██   ████    ████   ██    ▀█  ██   ▀██▄     ▄██▄     
          ██   ▄██  ██   ▄██   ██   █ ██   ▄█ ██   ██   █    ██   ▄██     ▄█▀██▄    
          ███████   ███████    ██   █  ██  █▀ ██   ██████    ███████     ▄█  ▀██    
          ██        ██  ██▄    ██   █  ██▄█▀  ██   ██   █  ▄ ██  ██▄     ████████   
          ██        ██   ▀██▄  ██   █  ▀██▀   ██   ██     ▄█ ██   ▀██▄  █▀      ██  
        ▄████▄    ▄████▄ ▄███▄████▄███▄ ▀▀  ▄████▄██████████████▄ ▄███▄███▄   ▄████▄
                                                                                                                      
                                       	
		Chromosome Data Provided On : 
                    
                    $params.filePath

                BLAT Database Provided On : 
                        
                    $params.blatdb
"""



process RUN_NUCMER_INTERCHROMOSOMAL {    


    container 'sadigngr/primera_designtest'

    input:
    tuple path(fa1), path(fa2)
        
    
    output:
    path "${fa1}+${fa2}.coords"

    
    script:
    """
    nucmer -c 200 -p ${fa1}+${fa2} $fa1 $fa2
    show-coords ${fa1}+${fa2}.delta > ${fa1}+${fa2}.coords
    """

}

process RUN_NUCMER_INTRACHROMOSOMAL {
    
    container 'sadigngr/primera_designtest'

    input:
    path fastaFile

    output:
    path "${fastaFile}+${fastaFile}.coords"

    script:
    """

    nucmer -c 200 -p $fastaFile+$fastaFile $fastaFile $fastaFile 
    show-coords ${fastaFile}+${fastaFile}.delta > ${fastaFile}+${fastaFile}.coords
    """

}

process PARSE_COORDS_INTERCHROMOSOMAL {
    
    container 'sadigngr/primera_designtest'

    input:
    path coordsfile
    
    output:
    path "*.locations"
     
    script:
    """ 
    awk -F'[|]' 'NF > 1 && \$0 !~ /^#/ {split(\$1,a," ");
    split(\$2,b," "); 
    S1=a[1]; E1=a[2]; S2=b[1]; 
    E2=b[2]; print S1, E1, S2, E2}' $coordsfile > ${coordsfile}.locations
    """
}

process PARSE_COORDS_INTRACHROMOSOMAL {
    
    container 'sadigngr/primera_designtest'

    input:
    path pre_coordsfile
    
    output:
    path "*.locations"
     
    script:
    """ 
    awk -F'[|]' 'NF > 1 && \$0 !~ /^#/ {split(\$1,a," ");
    split(\$2,b," "); 
    S1=a[1]; E1=a[2]; S2=b[1]; 
    E2=b[2]; print S1, E1, S2, E2}' $pre_coordsfile > ${pre_coordsfile}.pre
    
    python3 $baseDir/filter_coords.py ${pre_coordsfile}.pre > ${pre_coordsfile}.locations   

    """
}


process EXTRACT_FILES { 

    container 'sadigngr/primera_designtest'

    input:
    path location_files
    path filePath

    output:
    path "*.fa" 

    script:
    """
    python3 $baseDir/Extract.py ${location_files} ${filePath} > error.log 
    """

}

 process MERGE_EXTRACTS{


    container 'sadigngr/primera_designtest'

    input:
    path(bl_files, stageAs: "?/*")
    output:
    path "bl_input.fa"

    script:
    """
     cat ${bl_files.join(' ')} > bl_input.fa
    
    """

}

process RUN_BLAT {
     
    container 'sadigngr/primera_designtest'

    conda file("${baseDir}/environment.yml")

    input:
    path blinput
    path blat_db
    
    output:
    path "output.psl" 

    script:
    """
    blat $blat_db $blinput output.psl
    """

}

workflow {
    
    fasta_files_ch = Channel
        .fromPath("${params.filePath}/*.fa")

    fasta_files_for_pairwise = fasta_files_ch.collect()
    pairwise_ch = fasta_files_for_pairwise
        .flatMap { files -> 
            def pairs = []
            for (int i = 0; i < files.size(); i++) {
                for (int j = i+1; j < files.size(); j++) {
                    pairs << [files[i], files[j]]
                }
            }
            return pairs
        }
    
    nucmer_ch = RUN_NUCMER_INTERCHROMOSOMAL(pairwise_ch)
 
    nucmer_intra_ch = RUN_NUCMER_INTRACHROMOSOMAL(fasta_files_ch)
 
    parse_ch = PARSE_COORDS_INTERCHROMOSOMAL(nucmer_ch).flatten()
    
    parse_intra_ch = PARSE_COORDS_INTRACHROMOSOMAL(nucmer_intra_ch).flatten()
    
    parse_merged = parse_ch.mix(parse_intra_ch)

    extract_ch = EXTRACT_FILES(parse_merged, params.filePath)

    chList = extract_ch.collect() 
    
    merge_ch = MERGE_EXTRACTS(chList)
    
    blat_ch = RUN_BLAT(merge_ch, params.blatdb)
    
    println "The BLAT results can be found at: "
    blat_ch.view()
 
}
