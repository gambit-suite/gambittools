import logging
# import biopython to read in a fastq file
from Bio import SeqIO
import gzip
import os

class FilterFastq:
    """
    Reads in a FASTQ file using BioPython, identifies all kmers of length 11 beginning with ATGAC, creates a hash of these kmers and their frequencies, filters out all kmers with a frequency of 1, and writes the remaining kmers to a FASTA file.
    """
    def __init__(self, fastq_filename, kmer_prefix, kmer, min_kmer_freq, output_kmer_filename, verbose):
        """
    Initializes the FilterFastq class.
    Args:
      fastq_filename (str): The name of the FASTQ file to read.
      kmer_prefix (str): The prefix of the kmers to identify.
      kmer (int): The length of the kmers to identify.
      min_kmer_freq (int): The minimum frequency of kmers to keep.
      output_kmer_filename (str): The name of the FASTA file to write.
      verbose (bool): Whether to print debug messages.
    Side Effects:
      Initializes the logger, kmer_hash, kmer_count, and kmer_freq attributes.
    """
        self.logger = logging.getLogger(__name__)
        self.fastq_filename = fastq_filename
        self.kmer_prefix = kmer_prefix
        self.kmer = kmer
        self.min_kmer_freq = min_kmer_freq
        self.output_kmer_filename = output_kmer_filename
        self.verbose = verbose

        self.kmer_hash = {}
        self.kmer_count = 0
        self.kmer_freq = 0

        if self.verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.ERROR)

    def filter_fastq(self):
        """
    Reads in a FASTQ file, filters out kmers with a frequency of 1, and writes the remaining kmers to a FASTA file.
    """
        self.read_fastq()
        self.filter_kmers()
        self.write_kmers()

    # Read in a FASTQ file using BioPython
    def read_fastq(self):
        """
    Reads in a FASTQ file using BioPython.
    Args:
      self (FilterFastq): The FilterFastq instance.
    Side Effects:
      Iterates over the records and counts kmers.
    """
        logging.debug("Reading FASTQ file: %s", self.fastq_filename)

        # Get the file extension
        _, ext = os.path.splitext(self.fastq_filename)

        handle = self.fastq_filename
        # Open the file using the appropriate parser
        if ext == ".fa":
            parser = "fasta"
        elif ext == ".gz":
            parser = "fastq"
            handle = gzip.open(self.fastq_filename, "rt")
        else:
            parser = "fastq"

        # Iterate over the records and count k-mers
        for record in SeqIO.parse(handle, parser):
            seq = str(record.seq)
            self.count_kmers(seq)
            self.count_kmers(str(record.seq.reverse_complement()))
    
    # Count the kmers in the sequence
    def count_kmers(self, sequence):
        """
    Counts the kmers in the sequence.
    Args:
      self (FilterFastq): The FilterFastq instance.
      sequence (str): The sequence to count kmers in.
    Side Effects:
      Updates the kmer_count and kmer_hash attributes.
    """
        for i in range(len(sequence) - self.kmer + 1):
            kmer = sequence[i:i+self.kmer]
            if kmer.startswith(self.kmer_prefix):
                self.kmer_count += 1
                if kmer in self.kmer_hash:
                    self.kmer_hash[kmer] += 1
                else:
                    self.kmer_hash[kmer] = 1

    # Filter out kmers with a frequency of 1
    def filter_kmers(self):
        """
    Filters out kmers with a frequency of 1.
    Args:
      self (FilterFastq): The FilterFastq instance.
    Side Effects:
      Removes all values from the kmer_hash with a frequency of < min_kmer_freq.
    """
        logging.debug("Filtering kmers with a frequency of %s", self.min_kmer_freq)
        # Remove all values from the hash with a frequency of < self.min_kmer_freq
        for kmer in list(self.kmer_hash):
            if self.kmer_hash[kmer] < self.min_kmer_freq:
                del self.kmer_hash[kmer]

    # Write the kmers to a FASTA file
    def write_kmers(self):
        """
    Writes the kmers to a FASTA file.
    Args:
      self (FilterFastq): The FilterFastq instance.
    Side Effects:
      Writes the kmers to the output_kmer_filename.
    """
        logging.debug("Writing kmers to FASTA file: %s", self.output_kmer_filename)
        with open(self.output_kmer_filename, 'w') as output_file:
            # concat into a single mock sequence
            output_file.write(">from_file " + self.fastq_filename + "\n")
            for i, kmer in enumerate(self.kmer_hash):
                output_file.write(str(kmer) + "\n")
        logging.debug("Total kmers: %s", self.kmer_count)
        logging.debug("Total kmers with a frequency of %s: %s", self.min_kmer_freq, len(self.kmer_hash))
