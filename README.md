# CENG4217-Project
Python Scripts to benchmark SV Calling algorithms. 

illuminaBenchmark.py is used to benchmark to tardis, delly and manta. It runs
these tools sequentally and performs some measuerements about resource usages. 

nanoporeBenchmark.py is used to benchmark to cuteSV, SVIM and Sniffles. It runs
these tools sequentally and performs some measuerements about resource usages.

VCF files and plots for measured data will be outputs.

statsVCF.py is used to get statistics of different VCF files and write it to a single "result.txt" file.

### Requirements
- Python 3
- matplotlib, psutil and numpy libraries for python
  ##### For Illumına Benchmarking
    - [Tardis](https://github.com/BilkentCompGen/tardis "Tardis")
    - [Delly](https://github.com/dellytools/delly "Delly")
    - [Manta](https://github.com/Illumina/manta "Manta")
    - [bcftools](https://github.com/samtools/bcftools "bcftools")
  ##### For Nanopore Benchmarking
    - [cuteSV](https://github.com/tjiangHIT/cuteSV "cuteSV")
    - [SVIM](https://github.com/eldariont/svim "SVIM")
    - [Sniffles](https://github.com/fritzsedlazeck/Sniffles "Sniffles")
  ##### For Stats of VCFs
    - [SURVIVOR](https://github.com/fritzsedlazeck/SURVIVOR "SURVIVOR")
### How to install
``` bash 
git clone https://github.com/mertdgn/CENG4217-Project.git
```
### Running
  illuminaBenchmark.py
  ``` bash
  cd CENG4217-Project
  python3 illuminaBenchmark.py input.bam reference.fa sonicFile.sonic outputName
  ```
  nanoporeBenchmark.py
  ``` bash
  cd CENG4217-Project
  python3 nanoporeBenchmark.py input.bam reference.fa outputName
  ```
  statsVCF.py
  ``` bash
  #Make sure you collect the VCF files you want to compare statistics with in the same directory
  #Then go the directory and run the below command
  python3 /the/path/you/installed/CENG4217-Project/statsVCF.py
```


    
