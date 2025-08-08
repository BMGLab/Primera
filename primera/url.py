template_url = "https://genome.ucsc.edu/cgi-bin/hgPcr?hgsid=2900325362_8e48BzUFKDYcxxsPnAlLNmzHKyGA&org=Human&db=hg38&wp_target=genome&wp_f={f}&wp_r={r}&Submit=Submit&wp_size=300&wp_perfect=15&wp_good=15&boolshad.wp_flipReverse=0&wp_append=on&boolshad.wp_append=0"

input_file = "/home/musa/Desktop/Primera_mk/work/9b/3992f3e1375fef6fdc143c01275de2/primer_result_filtered.txt"

output_file = "primers_with_urls.txt"

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    header = next(infile)  
    outfile.write(header.strip() + "\t")  
    
    for line in infile:
        parts = line.strip().split("\t")
        if len(parts) < 4:
            outfile.write(line)  
            continue
        
        forward = parts[2]
        reverse = parts[3]
        url = template_url.format(f=forward, r=reverse)
        
        
        outfile.write(line.strip() + "\t" + url + "\n")
