import os
from src.utils.Data_Extraction_functions import write_lines_to_file

def process_files(input_directory):
    # Create output file paths
    esp_output_path = "./data/processed/esp_corpus.es"
    agr_output_path = "./data/processed/agr_corpus.agr"

    # Open the output files in append mode so that data is not overwritten
    with open(esp_output_path, 'a', encoding='utf-8') as esp_file, \
         open(agr_output_path, 'a', encoding='utf-8') as agr_file:
        
        # Dictionary to hold filenames with extensions
        file_dict = {}

        # Walk through the directory and subdirectories
        for root, _, files in os.walk(input_directory):
            for file in files:
                file_name, file_ext = os.path.splitext(file)
                
                # Only consider files with extensions .es and .agr
                if file_ext in ['.es', '.agr']:
                    file_path = os.path.join(root, file)
                    
                    # Add file paths to the dictionary for matching names
                    if file_name not in file_dict:
                        file_dict[file_name] = {}
                    file_dict[file_name][file_ext] = file_path

        # Now process the matched file pairs
        for file_name, extensions in file_dict.items():
            if '.es' in extensions and '.agr' in extensions:
                es_file_path = extensions['.es']
                agr_file_path = extensions['.agr']
                
                # Read the files and compare line counts
                with open(es_file_path, 'r', encoding='utf-8') as es_file, \
                     open(agr_file_path, 'r', encoding='utf-8') as ag_file:
                    es_lines = es_file.readlines()
                    agr_lines = ag_file.readlines()
                    
                    # If the number of lines match, write to output files
                    if len(es_lines) == len(agr_lines):
                        esp_file.writelines(es_lines)  # Write to the esp_output_path
                        agr_file.writelines(agr_lines)  # Write to the agr_output_path

def process_data():
    # Directories
    raw_dir = './data/raw'
    external_dir = './data/external'

    process_files(raw_dir)
    process_files(external_dir)
    
    print("Processing completed without problems.")

if __name__ == "__main__":
    process_data()