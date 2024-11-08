import os, random

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def save_to_file(sentences, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for sentence in sentences:
            file.write(sentence + "\n")

def process_files(input_directory: str):
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

def split_sentences(dir: str = 'processed_dir'):
    spanish_sentences = read_file(os.path.join(dir,'esp_corpus.es'))
    awajun_sentences = read_file(os.path.join(dir, 'agr_corpus.agr'))
    assert len(spanish_sentences) == len(awajun_sentences), "Mismatched number of sentences!"

    print(len(spanish_sentences),' - ', len(awajun_sentences))

    paired_sentences = list(zip(spanish_sentences, awajun_sentences))
    random.shuffle(paired_sentences)
    spanish_sentences, awajun_sentences = zip(*paired_sentences)

    split_ratio = 0.8
    split_index = int(len(spanish_sentences) * split_ratio)

    spanish_train = spanish_sentences[:split_index]
    spanish_test = spanish_sentences[split_index:]

    awajun_train = awajun_sentences[:split_index]
    awajun_test = awajun_sentences[split_index:]

    save_to_file(spanish_train, os.path.join(dir,'train','spanish_train.es'))
    save_to_file(spanish_test, os.path.join(dir,'test','spanish_test.es'))
    save_to_file(awajun_train, os.path.join(dir,'train','awajun_train.agr'))
    save_to_file(awajun_test, os.path.join(dir,'test','awajun_test.agr'))


def process_data():
    # Directories
    external_dir = './data/external'
    raw_dir = './data/preprocessed'
    processed_dir = './data/processed'
    
    process_files(external_dir)
    process_files(raw_dir)
    split_sentences(processed_dir)
        
    print("Processing completed without problems.")
    
if __name__ == "__main__":
    process_data()