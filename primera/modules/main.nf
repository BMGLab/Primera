

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

