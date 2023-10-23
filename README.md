# GAMBITtools
This repository contains a collection of tools for working with GAMBIT. The tools are written in Python and are designed to be used in conjunction with [GAMBIT](https://github.com/jlumpe/gambit/tree/master/gambit) (Genomic Approximation Method for Bacterial Identification and Tracking) which is a tool for rapid taxonomic identification of microbial pathogens.

# Installation

# Usage

## gambit-context

## gambit-core-check
This script takes in a GAMBIT database which has been compressed down to a core set of k-mers. It outputs the number of core k-mers found in one or more FASTA files provided as input. This gives a good indication of how much of the conserved GAMBIT k-mers of this species are present and thus lets you evaluate the quality of your assembly, since you will know what percentage of the core k-mers are present or missing. The input FASTA files can optionally be gzipped.

The script usage is:
```
usage: gambit-core-check [options]

Given a database of core gambit signatures and FASTA files, output the number and percentage of core kmers found

positional arguments:
  gambit_directory      A directory containing GAMBIT files (database and signatures)
  signatures_filename   A file containing the signatures
  database_filename     A file containing the sqlite database
  fasta_filenames       A list of FASTA files of genomes

options:
  -h, --help            show this help message and exit
  --extended, -e        Extended output (default: False)
  --cpus CPUS, -p CPUS  Number of cpus to use (default: 1)
  --kmer KMER, -k KMER  Length of the k-mer to use (default: 11)
  --kmer_prefix KMER_PREFIX, -f KMER_PREFIX
                        Kmer prefix (default: ATGAC)
  --verbose, -v         Turn on verbose output (default: False)
```

A default output has is a tab delimited table of the format:
| Filename                | Species                    | Completeness (%) |
|-------------------------|----------------------------|------------------|
| GCA_000007325.1.fna.gz  | Fusobacterium nucleatum    | 100.00%          |
| GCA_000007385.1.fna.gz  | Xanthomonas oryzae         | 100.00%          |
| GCA_000008525.1.fna.gz  | Helicobacter pylori        | 85.00%           |
| GCA_000011445.1.fna.gz  | Mycoplasma mycoides        | 100.00%          |
| GCA_000013525.1.fna.gz  | Streptococcus pyogenes     | 99.85%           |
| GCA_000013965.1.fna.gz  | Leptospira borgpetersenii  | 100.00%          |
| GCA_000014325.1.fna.gz  | Streptococcus suis         | 98.91%           |
| GCA_000015425.1.fna.gz  | Acinetobacter baumannii    | 97.61%           |
| GCA_000016205.1.fna.gz  | Burkholderia vietnamiensis | 99.61%           |


And the extended output is a tab delmiited table of the format:
| Filename                 | Species                   | Completeness (%) | Core kmers     | Closest accession | Closest distance |
|--------------------------|---------------------------|------------------|----------------|-------------------|------------------|
| GCA_000014325.1.fna.gz   | Streptococcus suis        | 98.91%           | (363/367)      | GCF_000440895.1   | 0.9206           |
| GCA_000015425.1.fna.gz   | Acinetobacter baumannii   | 97.61%           | (1879/1925)    | GCF_001576615.1   | 0.7848           |
| GCA_000016205.1.fna.gz   | Burkholderia vietnamiensis| 99.61%           | (2318/2327)    | GCF_000959445.1   | 0.7700           |
| GCA_000016465.1.fna.gz   | Haemophilus influenzae    | 100.00%          | (359/359)      | GCF_000016465.1   | 0.8544           |
| GCA_000018925.1.fna.gz   | Francisella tularensis    | 100.00%          | (1158/1158)    | GCF_000833355.1   | 0.5407           |
| GCA_000020605.1.fna.gz   | Agathobacter rectalis     | 100.00%          | (895/895)      | GCA_000020605.1   | 0.8829           |
| GCA_000022825.1.fna.gz   | Yersinia pestis           | 99.93%           | (7172/7177)    | GCF_000324405.1   | 0.2955           |
| GCA_000027065.2.fna.gz   | Cronobacter turicensis    | 100.00%          | (4393/4393)    | GCA_000027065.2   | 0.5175           |
| GCA_000027305.1.fna.gz   | Haemophilus influenzae    | 100.00%          | (359/359)      | GCF_000016465.1   | 0.8587           |

## gambit-database-recall
This script checks to see if the classification output of GAMBIT is inline with the genomes used to make the GAMBIT database used. An assembly metadata spreadsheet is provided, which is generated with creating a GAMBIT database.  The script also takes the output of running GAMBIT over a set of genomes. The results of the Genus/Species calls from GAMBIT are compared to the assembly metadata spreadsheet and statistics are outputted 

Input assembly metadata spreadsheet format (comma delimited):
| uuid            | species_taxid | assembly_accession | species                |
|-----------------|---------------|--------------------|------------------------|
| GCA_000277025.1 | 1             | GCA_000277025.1    | Legionella pneumophila |
| GCA_000277065.1 | 1             | GCA_000277065.1    | Legionella pneumophila |
| GCA_000300315.1 | 2             | GCA_000300315.1    | Coxiella burnetii      |
| GCA_000359545.5 | 2             | GCA_000359545.5    | Coxiella burnetii      |

The GAMBIT results format (comma delimited):
| query           | predicted.name       | predicted.rank | predicted.ncbi_id | predicted.threshold | closest.distance | closest.description | next.name | next.rank | next.ncbi_id | next.threshold |
|-----------------|----------------------|----------------|--------------------|----------------------|------------------|---------------------|-----------|-----------|--------------|----------------|
| GCA_000277025.1 | Legionella pneumophila | species        | 1                  | 1.0                  | 0.0              |                     |           |           |              |                |
| GCA_000277065.1 | Legionella pneumophila | species        | 1                  | 1.0                  | 0.0              |                     |           |           |              |                |
| GCA_000300315.1 | Coxiella burnetii      | species        | 2                  | 0.9998               | 0.0              |                     |           |           |              |                |
| GCA_000359545.5 | Coxiella burnetii      | species        | 2                  | 0.9998               | 0.0              |                     |           |           |              |                |

The script gives a summary of the recall of the database. Every genome in the database should be recalled accurately if provided again:
```
Number of species: 2902
Number of samples: 5062
Correct species calls: 2874     (56.7%)
Number of no calls: 2181        (43.0%)
Number of no calls where genus matches in next: 1068    (21.0%)
Number of incorrect genus calls: 1113   (21.92%)
Number of genus only calls: 4   (0.07%)
Number of incorrect genus calls: 0      (0.0%)
Number of incorrect species calls: 3    (0.05%)
```

Additionally if there are inconsistencies in the species calls, these will be outputted for further investigation:

| ID   | species                          | predicted.name                  | assembly_accession | next.name |
|------|----------------------------------|---------------------------------|--------------------|-----------|
| 2306 | Cuniculiplasma sp023489425       | Cuniculiplasma divulgatum       | GCA_023489425.1    | NaN       |
| 87   | Methanothermobacter sp000828575  | Methanothermobacter thermautotrophicus | GCF_000828575.1 | NaN       |
| 1961 | Nitrosopelagicus sp013390745     | Nitrosopelagicus sp000402075     | GCA_013390745.1    | NaN       |

Two files output extended information on the species recall, allowing you to dig further into them, correct_incorrect_predictions.txt and correct_incorrect_predictions.txt.differences.csv files.

## gambit-filter-fastq

## gambit-list-taxa

## gambit-test-random-data

# Papers and citation
Please cite the following paper if you use this software:
    
```
    Lumpe J, Gumbleton L, Gorzalski A, Libuit K, Varghese V, et al. (2023) GAMBIT (Genomic Approximation Method for Bacterial Identification and Tracking): A methodology to rapidly leverage whole genome sequencing of bacterial isolates for clinical identification. PLOS ONE 18(2): e0277575. https://doi.org/10.1371/journal.pone.0277575
```

If you use the Eukaryote database please cite:
```
Ambrosio FJ 3rd, Scribner MR, Wright SM, Otieno JR, Doughty EL, Gorzalski A, Siao DD, Killian S, Hua C, Schneider E, Tran M, Varghese V, Libuit KG, Pandori M, Sevinsky JR, Hess D. TheiaEuk: a species-agnostic bioinformatics workflow for fungal genomic characterization. Front Public Health. 2023 Aug 1;11:1198213. doi: https://doi.org/10.3389/fpubh.2023.1198213. PMID: 37593727; PMCID: PMC10428623.
```


# Licence
GAMBITtools is open source software released under the GNU General Public License (GPL) version 3.0. See the file [LICENSE](LICENSE) for details.

# Support
This open source software is provided for free without support. 
Paid support is available from [Theiagen Genomics] (https://www.theiagen.com/).


