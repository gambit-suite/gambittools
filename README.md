# GAMBITtools
This repository contains a collection of tools for working with GAMBIT. The tools are written in Python and are designed to be used in conjunction with [GAMBIT](https://github.com/gambit-suite/gambit) (Genomic Approximation Method for Bacterial Identification and Tracking) which is a tool for rapid taxonomic identification of microbial pathogens.

# Installation
The GAMBITtools scripts are written in Python and require Python 3.6 or higher.  The scripts have been tested on Linux (Ubuntu 22.04).  The scripts have the following dependancies:

* gambit 
* pandas
* numpy
* sqlite3
* SeqIO (Biopython)
* gzip

To install the software, run the following command:
```
pip install git+https://github.com/gambit-suite/gambittools.git
```

## Docker
You can use docker to run the software.  To build from scratch run:
```
docker build -t gambittools .
```
then to run one of the scripts:
```
docker run -v $(pwd):/data gambittools gambit-list-taxa /data/gambit_database.gdb
```

# Usage          |

## gambit-database-recall
This script checks to see if the classification output of GAMBIT is inline with the genomes used to make the GAMBIT database used. An assembly metadata spreadsheet is provided, which is generated with creating a GAMBIT database.  The script also takes the output of running GAMBIT over a set of genomes. The results of the Genus/Species calls from GAMBIT are compared to the assembly metadata spreadsheet and statistics are outputted 

The script usage is:
```
usage: gambit-database-recall [options]

Work out how good a GAMBIT database is at recalling species when the training set is passed in

positional arguments:
  assembly_metadata_spreadsheet
                        Assembly metadata file such as assembly_metadata.csv from the gambit-gtdb script
  gambit_results_file   Gambit results file where the accessions match the GTDB file

options:
  -h, --help            show this help message and exit
  --output_filename OUTPUT_FILENAME, -o OUTPUT_FILENAME
                        Output filename (default: correct_incorrect_predictions.txt)
  --debug               Turn on debugging (default: False)
  --verbose, -v         Turn on verbose output (default: False)
```

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
This preprocesing script takes in a FASTQ file, identifies the reads that contain GAMBIT k-mers (forward and reverse) and outputs a FASTA file which just contains those k-mer sequences. A minimum k-mer coverage an be specified to filter out low coverage k-mers, which may be due to sequencing errors. The input FASTQ file can optionally be gzipped.  The output FASTA file can then be used as input to GAMBIT will allows for FASTA files as input.  Whilst k-mers are likely to be split across reads, the default GAMBIT k-mer size and target (16 bases) is small enough to work with the most commonly used Illumina sequencing platforms which produce reads of 150 bases or more.  

The script usage is:
```
usage: gambit-filter-fastq [options]

Filter a FASTQ file to remove low abundance kmers, and save as an efficient FASTA file for input to GAMBIT

positional arguments:
  fastq_filename        Input FASTQ file

options:
  -h, --help            show this help message and exit
  --kmer_prefix KMER_PREFIX, -p KMER_PREFIX
                        Kmer prefix (default: ATGAC)
  --kmer KMER, -k KMER  Length of the k-mer to use (default: 16)
  --min_kmer_freq MIN_KMER_FREQ, -f MIN_KMER_FREQ
                        Minimum kmer frequency (default: 2)
  --output_kmer_filename OUTPUT_KMER_FILENAME, -o OUTPUT_KMER_FILENAME
                        Output filename for filtered FASTA containing only kmers (default: filtered_kmers.fa)
  --debug               Turn on debugging (default: False)
  --verbose, -v         Turn on verbose output (default: False)
```

The output file defaults to filtered_kmers.fa and just contains the kmers. There is a very small chance that a false k-mer could be constructed from the k-mers in this format, however it is unlikely to have a high enough frequency to be called by GAMBIT, which is quite robust to noise.  The output file is a FASTA file of the format:
```
>from_file test.fastq
ATGACCCGCTA
ATGACCTCTGT
ATGACTGTTAT
ATGACCCGAGG
ATGACGCCCTG
ATGACCGGATC
ATGACCGCTGG
ATGACAGATCC
```

You can then run GAMBIT as normal on the file filtered_kmers.fa:
```
gambit -d database_directory query filtered_kmers.fa
```

## gambit-list-taxa
This script will take in a GAMBIT database file and list the taxa in the database.  The default is to list the species, but the genus can also be listed.  Extended information about each species is available including how many genomes are found within a species.

The script usage is:
```
usage: gambit-list-taxa [options]

List the taxa in a gambit database

positional arguments:
  database_main_filename
                        A database .gdb file created by gambit build

options:
  -h, --help            show this help message and exit
  --rank RANK, -r RANK  taxonomic rank (genus/species) (default: species)
  --extended, -e        Extended output (default: False)
  --verbose, -v         Turn on verbose output (default: False)
```

The default output is a list of species:
```
Abiotrophia defectiva
Abyssicoccus albus
Acaryochloris marina_A
Acetatifactor intestinalis
Acetatifactor muris
Acetobacter aceti
Acetobacter ascendens
Acetobacter cerevisiae
Acetobacter fabarum
Acetobacter ghanensis
...
```

The extended output is a tab delimited table of the format:
| Species                   | Distance threshold       | No. Genomes | No. Child taxa | Curation version |
|---------------------------|--------------------------|-------------|----------------|------------------|
| Abiotrophia defectiva     | 0.0009                   | 2           | 0              | GTDB             |
| Abyssicoccus albus        | 0.4038                   | 2           | 1              | GTDB             |
| Acaryochloris marina_A    | 0.4585                   | 2           | 0              | GTDB             |
| Acetatifactor intestinalis| 0.6511                   | 9           | 2              | GTDB             |
| Acetatifactor muris       | 0.0022                   | 2           | 0              | GTDB             |
| Acetobacter aceti         | 0.0335682146251201       | 3           | 0              | Original         |
| Acetobacter ascendens     | 0.5318                   | 8           | 0              | GTDB             |
| Acetobacter cerevisiae    | 0.5857046842575073       | 3           | 0              | Original         |
| Acetobacter fabarum       | 0.4983                   | 6           | 0              | GTDB             |

The distance_threshold is the GAMBIT diameter for the species. The number of genomes is the number of genomes in the database for that species. The curation version indicates whether the species was curated by the original published NCBI taxonomy or by the recent automated GTDB taxonomy.
Where there are child taxa, these are the number of species that are found within the species.  For example, a species could have a total of 9 genomes in the database, but these could be split into 2 subspecies, with 7 genomes in one subspecies and 2 genomes in another subspecies.
When looking at the genus rank, the total number of genomes will be all the direct child taxa (usually the species, but not the subspecies). There are a few conditions not covered, where more complex structures were curated to reflect the needs of public health in the taxonomy, such as for E. coli/Shigella and Enterobacter cloacae.

## gambit-test-random-data
This helper script will create a random FASTA file containing GAMBIT k-mers for testing. It can be run with the defaults and no other input parameters.

The script usage is:
```
usage: gambit-test-random-data [options]

Create a random file containing gambit k-mers for testing

positional arguments:
  output_filename       Output filename

options:
  -h, --help            show this help message and exit
  --num_kmers NUM_KMERS, -n NUM_KMERS
                        Number of k-mers (default: 50)
  --kmer KMER, -k KMER  Length of the k-mer to use (default: 11)
  --kmer_prefix KMER_PREFIX, -f KMER_PREFIX
                        Kmer prefix (default: ATGAC)
```

## gambit-context
In development.

# Tests
The unit tests can be run with the following command:
```
python3 -m unittest discover -s gambittools/tests/ -p '*_test.py'
```

# Papers and citation
Please cite the following paper if you use this software:
    
```
    Lumpe J, Gumbleton L, Gorzalski A, Libuit K, Varghese V, et al. (2023) GAMBIT (Genomic Approximation Method for Bacterial Identification and Tracking): A methodology to rapidly leverage whole genome sequencing of bacterial isolates for clinical identification. PLOS ONE 18(2): e0277575. doi: [10.1371/journal.pone.0277575](https://doi.org/10.1371/journal.pone.0277575).
```

If you use the Fungal database (TheiaEuk) please cite:
```
Ambrosio FJ 3rd, Scribner MR, Wright SM, Otieno JR, Doughty EL, Gorzalski A, Siao DD, Killian S, Hua C, Schneider E, Tran M, Varghese V, Libuit KG, Pandori M, Sevinsky JR, Hess D. TheiaEuk: a species-agnostic bioinformatics workflow for fungal genomic characterization. Front Public Health. 2023 Aug 1;11:1198213. doi: [10.3389/fpubh.2023.1198213](https://doi.org/10.3389/fpubh.2023.1198213). PMID: 37593727; PMCID: PMC10428623.
```

# Licence
GAMBITtools is open source software released under the GNU General Public License (GPL) version 3.0. See the file [LICENSE](LICENSE) for details.

# Support
This open source software is provided for free without support. 
Paid support is available from [Theiagen Genomics](https://www.theiagen.com/).
