# Primera
Primera Multi-Target Primer Designing Pipeline

## usage


nextflow run main.nf \
  --container primera-pipeline:latest \
  --filePath /path/to/.fa
  --blatdb   /path/to/hg38.2bit


nextflow run designPrimers.nf \
  --container primera-pipeline:latest \
  --pslFile /path/to/file.psl \
  --blatdb /path/to/hg38.2bit \
  --filtered_chrs chr13,chr18,chr21,chr2

