# a class which takes in 2 spreadsheets, assembly_metadata_spreadsheet and gambit_results_file, then compares them with pandas
# so that we can work out how good gambit is at recalling species. The column they are joined on is the 
# accession number which is the first column in both spreadsheets. The species column from the assembly_metadata_spreadsheet needs to be compared to the equivalent predicted.name column in the gambit_results_file.
#The spreadsheets are in the following formats.
#assembly_metadata_spreadsheet file format:
# uuid,species_taxid,assembly_accession,species
# GCA_000277025.1,1,GCA_000277025.1,Legionella pneumophila
# GCA_000277065.1,1,GCA_000277065.1,Legionella pneumophila
# GCA_000300315.1,2,GCA_000300315.1,Coxiella burnetii
# GCA_000359545.5,2,GCA_000359545.5,Coxiella burnetii
#
#gambit_results_file file format:
# query,predicted.name,predicted.rank,predicted.ncbi_id,predicted.threshold,closest.distance,closest.description,next.name,next.rank,next.ncbi_id,next.threshold
# GCA_000277025.1,Legionella pneumophila,species,1,1.0,0.0,,,,,
# GCA_000277065.1,Legionella pneumophila,species,1,1.0,0.0,,,,,
# GCA_000300315.1,Coxiella burnetii,species,2,0.9998,0.0,,,,,
# GCA_000359545.5,Coxiella burnetii,species,2,0.9998,0.0,,,,,

import pandas as pd
import logging

class DatabaseRecall:
    """
    Compares two spreadsheets to work out how good Gambit is at recalling species.
    """
    def __init__(self, assembly_metadata_spreadsheet, gambit_results_file, output_filename, debug, verbose):
        """
    Initializes the DatabaseRecall class.
    Args:
      assembly_metadata_spreadsheet (str): The path to the assembly metadata spreadsheet.
      gambit_results_file (str): The path to the Gambit results file.
      output_filename (str): The path to the output file.
      debug (bool): Whether to enable debug logging.
      verbose (bool): Whether to enable verbose logging.
    Side Effects:
      Initializes the logger.
    """
        self.assembly_metadata_spreadsheet = assembly_metadata_spreadsheet
        self.gambit_results_file = gambit_results_file
        self.output_filename = output_filename
        self.debug = debug
        self.verbose = verbose

        self.logger = logging.getLogger('DatabaseRecall')
        self.logger.debug('DatabaseRecall.__init__')

    def compare_results(self):
        """
    Compares the species column from the assembly_metadata_spreadsheet to the predicted.name column in the gambit_results_file.
    Args:
      None
    Returns:
      None
    Side Effects:
      Prints the number of correct and incorrect predictions.
      Writes the output to the output_filename.
    Examples:
      >>> compare_results()
      Indentical predictions: 3
      Percentage identical: 75.0%
    """
        self.logger.debug('DatabaseRecall.compare_results')
        # Read in the assembly metadata spreadsheet
        assembly_metadata = pd.read_csv(self.assembly_metadata_spreadsheet)
        # Read in the gambit results file
        gambit_results = pd.read_csv(self.gambit_results_file)
        num_samples = gambit_results.shape[0]
        
        # if the species name end in 'subspecies X' in assembly_metadata, replace remove it
        assembly_metadata['species'] = assembly_metadata['species'].str.replace(' subspecies \d+', '', regex=True)

        # Join the two spreadsheets on the accession number
        joined = pd.merge(assembly_metadata, gambit_results, left_on='assembly_accession', right_on='query')
        # Compare the species column from the assembly_metadata spreadsheet to the predicted.name column in the gambit_results file
        joined['correct'] = joined['species'] == joined['predicted.name']

        # count the number of unique species names
        num_species = joined['species'].nunique()
        print('Number of species: ' + str(num_species))
        print('Number of samples: ' + str(num_samples))

        correct = 0
        incorrect = 0
        # Count the number of correct and incorrect predictions
        # check if joined['correct'] contains a true value
        if joined['correct'].any():
            correct = joined['correct'].value_counts()[True]
        
        #if not joined['correct'].any():
        #    incorrect = joined['correct'].value_counts()[False]

        # Print the number of correct and incorrect predictions

        # Calculate the percentage of correct predictions
        percentage_correct = correct/(num_samples)*100
        print('Correct species calls: ' + str(correct) + '\t('+str((correct/num_samples)*100) + '%)')

        output_df = joined[['species', 'predicted.name', 'assembly_accession']]
        output_df.to_csv(self.output_filename, index=False)

        # select rows where correct is True
        incorrect_df = joined[joined['correct'] == False]
        incorrect_df = incorrect_df[['species', 'predicted.name', 'assembly_accession','next.name']]
        # sort by species
        incorrect_df = incorrect_df.sort_values(by=['species'])
        incorrect_df.to_csv(self.output_filename + '.differences.csv', index=False)

        # figure out why these calls werent made.
        # count the number of rows in incorrect_df where the predicted.name was empty
        no_call = incorrect_df[incorrect_df['predicted.name'].isnull()]
        print('Number of no calls: ' + str(no_call.shape[0]) + '\t('+str((no_call.shape[0]/num_samples)*100) + '%)')
        num_no_call = no_call.shape[0]

        # get the first word of the species name and add it to partial_call as a new column called actual_genus
        no_call['actual_genus'] = no_call['species'].str.split(' ').str[0]
        # count the number of rows where the predicted.name is the same as the actual_genus
        no_call = no_call[no_call['next.name'] == no_call['actual_genus']]
        print('Number of no calls where genus matches in next: ' + str(no_call.shape[0]) + '\t('+str((no_call.shape[0]/num_samples)*100) + '%)')
        incorrect_genus = num_no_call - no_call.shape[0]
        print('Number of incorrect genus calls: ' + str(incorrect_genus) + '\t('+str((incorrect_genus/num_samples)*100) + '%)')

        # count the number of predicted.name rows that did not contain a space and the string is a substring of the species name
        # e.g. predicted.name = 'Legionella' and species = 'Legionella pneumophila'
        # count the number of rows in incorrect_df where the predicted.name was empty
        partial_call = incorrect_df[incorrect_df['predicted.name'].str.contains(' ') == False]
        genus_only_calls = partial_call.shape[0]
        # get the first word of the species name and add it to partial_call as a new column called actual_genus
        partial_call['actual_genus'] = partial_call['species'].str.split(' ').str[0]
        # count the number of rows where the predicted.name is the same as the actual_genus
        partial_call = partial_call[partial_call['predicted.name'] == partial_call['actual_genus']]
        
        print('Number of genus only calls: ' + str(partial_call.shape[0]) + '\t('+str((partial_call.shape[0]/num_samples)*100) + '%)')
        incorrect_genus = genus_only_calls - partial_call.shape[0]
        print('Number of incorrect genus calls: ' + str(incorrect_genus) + '\t('+str((incorrect_genus/num_samples)*100) + '%)')

        # count the number of incorrect species calls
        partial_call = incorrect_df[incorrect_df['predicted.name'].str.contains(' ') == True]
        incorrect_species = partial_call.shape[0]
        print('Number of incorrect species calls: ' + str(incorrect_species) + '\t('+str((incorrect_species/num_samples)*100) + '%)')
        print(partial_call)
        

