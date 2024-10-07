import re
from collections import Counter
import string

def count_words_in_file(input_file, output_file):
    # Open the input file and read its content
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Combine standard punctuation and additional punctuation
    all_punctuation = string.punctuation + "-'¡¿"
    
    # Create a regex pattern to remove punctuation
    text = re.sub(f'[{re.escape(all_punctuation)}]', '', text)

    # Tokenize the words by splitting on whitespace and convert to lowercase
    words = text.lower().split()  # Convert to lowercase here

    # Count the occurrences of each word
    word_counts = Counter(words)

    # Write the word counts to a TSV file
    with open(output_file, 'w', encoding='utf-8') as out_f:
        # Write word counts
        for word, count in word_counts.items():
            out_f.write(f"{word}\t{count}\n")
