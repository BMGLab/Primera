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



process RUN_NUCMER {    

    container 'staphb/mummer'

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

process PARSE_COORDS {
    
    input:
    path coordsfile
    
    output:
    path "${coordsfile}.locations"
    
    
    script:
    """ 
    awk -F'[|]' 'NF > 1 && \$0 !~ /^#/ {split(\$1,a," ");
    split(\$2,b," "); 
    S1=a[1]; E1=a[2]; S2=b[1]; 
    E2=b[2]; print S1, E1, S2, E2}' $coordsfile > ${coordsfile}.locations
    """
}

process EXTRACT_FILES { 

    conda file("${baseDir}/environment.yml")

    input:
    val location_files
    path filePath

    output:
    path "*.bl" 

    script:
    """
    python3 $baseDir/Extract.py $location_files $filePath 
    """

}

 process MERGE_EXTRACTS{

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

    input:
    path blinput
    
    output:
    stdout

    script:
    """
    echo $blinput
    """
}

workflow {

    fasta_files_ch = Channel
        .fromPath("${params.filePath}/*.fa")
        .collect()

    pairwise_ch = fasta_files_ch
        .flatMap { files -> 
            def pairs = []
            for (int i = 0; i < files.size(); i++) {
                for (int j = i+1; j < files.size(); j++) {
                    pairs << [files[i], files[j]]
                }
            }
            return pairs
        }
 
    nucmer_ch = RUN_NUCMER(pairwise_ch) | PARSE_COORDS
   
    extract_ch = EXTRACT_FILES(nucmer_ch, params.filePath)

    chList = extract_ch.collect() 
    
    merge_ch = MERGE_EXTRACTS(chList) | RUN_BLAT
    
    
    
    println "The BLAT results can be found on: "
    merge_ch.view()
 
}
