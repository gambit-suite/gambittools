# tests for the FilterFastq class
import unittest
import os
import filecmp
import tempfile
from gambittools.FilterFastq  import FilterFastq

test_modules_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(test_modules_dir, 'data','filter_fastq')

class TestFilterFastq(unittest.TestCase):
    """
    Test class for the FilterFastq class.
    """
    def test_filter_fastq(self):
        """
    Tests the filter_fastq method of the FilterFastq class.
    Args:
      self (TestFilterFastq): The TestFilterFastq instance.
    Side Effects:
      Creates and deletes files in the data_dir.
    Notes:
      Asserts that the output file is equal to the expected output file.
    """
        self.cleanup()
        fastq_filename = os.path.join(data_dir, 'test.fastq')
        kmer_prefix = 'ATGAC'
        kmer = 11
        min_kmer_freq = 2

        with tempfile.TemporaryDirectory() as temp_dir:
            output_kmer_filename = os.path.join(temp_dir, 'test_output_kmers.fa')

            verbose = False

            f = FilterFastq(fastq_filename,
                        kmer_prefix,
                        kmer,
                        min_kmer_freq,
                        output_kmer_filename,
                        verbose)
            f.filter_fastq()
            self.assertTrue(filecmp.cmp(output_kmer_filename, os.path.join(data_dir, 'test_expected_output_kmers.fa'), shallow=False))
            self.cleanup()

    def cleanup(self):
        """
    Deletes any existing output files in the data_dir.
    Args:
      self (TestFilterFastq): The TestFilterFastq instance.
    Side Effects:
      Deletes files in the data_dir.
    """
        for f in ['test_output_kmers.fa']:
            if os.path.exists(os.path.join(data_dir, f)):
                os.remove(os.path.join(data_dir, f))  