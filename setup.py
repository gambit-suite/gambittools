import os
import glob
from setuptools import setup, find_packages

def read(fname):
    """
    Reads a file.
    Args:
      fname (str): The name of the file to read.
    Returns:
      str: The contents of the file.
    Examples:
      >>> read('README.md')
      'This is the contents of the README.md file.'
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = '1.0.0'
if os.path.exists('VERSION'):
  version = open('VERSION').read().strip()

setup(
    name='gambittools',
    version=version,
    description='GAMBITtools: a collection of helper scripts for working with GAMBIT',
	long_description=read('README.md'),
    packages = find_packages(),
    author='Andrew J. Page',
    author_email='andrew.page@theiagen.com',
    url='https://github.com/gambit-suite/gambit-tools',
    scripts=glob.glob('scripts/*'),
    test_suite='nose.collector',
    tests_require=['nose >= 1.3'],
    install_requires=[
           'biopython >= 1.68',
           'pandas',
           'numpy',
           'db-sqlite3'

       ],
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
		    'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
)