import os
import pypdf
import re
import unicodedata

from ..utils.Data_Extraction_functions import get_file_path

class DictionaryEntry:
    def __init__(self, word: str, grammatical_category: str, meaning: str):
        """Inicializa una entrada del diccionario.

        Args:
            word (str): La palabra de la entrada.
            grammatical_category (str): La categoría gramatical de la palabra.
            meaning (str): El significado de la palabra.
        """
        self.word = word
        self.grammatical_category = grammatical_category
        self.meaning = meaning

    def __repr__(self) -> str:
        """Representa la entrada del diccionario como una cadena.

        Returns:
            str: Representación de la entrada del diccionario.
        """
        return f"{self.word} ({self.grammatical_category}): {self.meaning}"
    
def extract_pages(reader: pypdf.PdfReader, init: int, end: int) -> list[str]:
    """Extrae texto de páginas específicas de un lector de PDF.

    Args:
        reader (pypdf.PdfReader): El lector de PDF.
        init (int): El índice inicial de la página.
        end (int): El índice final de la página.

    Returns:
        list[str]: Una lista de cadenas que contiene el texto extraído de las páginas.
    """
    pages = []
    for i in range(init, end):
        page = reader.pages[i]
        pages.append(page.extract_text())
    return pages

def pages_to_string(pdf_pages: list[str]) -> str:
    """Convierte una lista de páginas de texto en una sola cadena.

    Args:
        pdf_pages (list[str]): Lista de texto de las páginas.

    Returns:
        str: Texto concatenado de todas las páginas.
    """
    return ''.join(pdf_pages)

def remove_prefix_phrases_and_last_line(text_list: list[str]) -> list[str]:
    """Elimina frases prefijo y la última línea de cada texto en la lista.

    Args:
        text_list (list[str]): Lista de cadenas de texto.

    Returns:
        list[str]: Lista de cadenas de texto después de la limpieza.
    """
    prefix_pattern = r"^(FORMABIAP\s*-\s*AIDESEP\s*-\s*ISEPL\d*|Diccionario\s*Awajún\d*)"
    lastLine_pattern = r"\n\w+$"

    cleaned_list = []

    for text in text_list:
        cleaned_text = re.sub(prefix_pattern, "", text).strip()
        cleaned_text = re.sub(lastLine_pattern, "", cleaned_text)
        cleaned_list.append(cleaned_text)

    return cleaned_list

def search_dictionary_entries(text_list: list[str]) -> list[str]:
    """Busca entradas del diccionario en el texto proporcionado.

    Args:
        text_list (list[str]): Lista de cadenas de texto.

    Returns:
        list[str]: Lista de palabras encontradas en el texto.
    """
    full_text = "\n".join(text_list)
    full_text = full_text.replace("\n", " ")
    full_text = ' '.join(full_text.split())

    pattern = r'(\w+ (s\.|adj\.|adv\.|conj\.|interj\.|onom\.|interr\.|pron\.|v\.))'
    entries = re.findall(pattern, full_text)

    result = [entry[0] for entry in entries]

    return result

def process_dictionary_entries(text_list: list[str]) -> list[DictionaryEntry]:
    """Procesa las entradas del diccionario a partir de una lista de texto.

    Args:
        text_list (list[str]): Lista de cadenas de texto.

    Returns:
        list[DictionaryEntry]: Lista de objetos DictionaryEntry procesados.
    """
    # Combine the list of text entries into a single string
    full_text = "\n".join(text_list)
    full_text = full_text.replace("\n", " ")
    full_text = ' '.join(full_text.split())

    # Regular expression pattern to capture word and meaning
    pattern = r'(\w+ (s\.|adj\.|adv\.|conj\.|interj\.|onom\.|interr\.|pron\.|v\.))(.*?)(?=\w+ (s\.|adj\.|adv\.|conj\.|interj\.|onom\.|interr\.|pron\.|v\.))'
    entries_with_text = re.findall(pattern, full_text, re.DOTALL)

    # Initialize the dictionary to store word-meaning pairs

    dictionary = []
    
    for entry in entries_with_text:
        word = entry[0].strip().split()[0]
        grammatical_category = entry[0].strip().split()[1]
        meaning = entry[2].strip()
        
        # Add the cleaned word and its meaning to the dictionary
        
        dictionary.append(DictionaryEntry(word, grammatical_category, meaning))

    return dictionary

def remove_accents(input_str: str) -> str:
    """Elimina los acentos de una cadena.

    Args:
        input_str (str): La cadena de entrada.

    Returns:
        str: La cadena sin acentos.
    """
    input_str = input_str.lower()
    return ''.join(c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn')

def process_meaning(word: str, meaning: str, grammatical_category: str) -> tuple[list[str], list[str], list[str]]:
    """Procesa el significado de una palabra y extrae oraciones relevantes.

    Args:
        word (str): La palabra a procesar.
        meaning (str): El significado de la palabra.
        grammatical_category (str): La categoría gramatical de la palabra.

    Returns:
        tuple[list[str], list[str], list[str]]: Tres listas de oraciones: mono_agr, agr_sentences y es_sentences.
    """
    meaning = meaning.replace("||", "").strip()
    meaning = re.sub(r'[¡!¿?]', '.', meaning)

    sentences = re.split(r'\.\s*', meaning)
    sentences = [s.strip() for s in sentences if s.strip()]

    mono_agr = []
    if len(sentences) >= 2:
        first_two_sentences = sentences[:2]
        mono_agr = [first_two_sentences[0], first_two_sentences[1]]
    
    agr_sentences = []
    es_sentences = []

    search_word = word[:4] if grammatical_category == 'v.' and len(word) >= 4 else word
    search_word = remove_accents(search_word)

    i = 2
    while i < len(sentences):
        sentence = remove_accents(sentences[i])
        if re.search(rf'{re.escape(search_word)}\w*', sentence):
            if(i != len(sentences)-1):
                agr_sentences.append(sentences[i])
            if i + 1 <len(sentences):
                es_sentences.append(sentences[i + 1])
            i += 2
        else:
            i += 1

    return mono_agr, agr_sentences, es_sentences

def process_multiple_entries(entries: list[DictionaryEntry]) -> tuple[list[str], list[str], list[str]]:
    """Procesa múltiples entradas del diccionario y agrupa oraciones relevantes.

    Args:
        entries (list[DictionaryEntry]): Lista de entradas del diccionario.

    Returns:
        tuple[list[str], list[str], list[str]]: Tres listas de oraciones: mono_agr_all, agr_sentences_all y es_sentences_all.
    """
    mono_agr_all = []
    agr_sentences_all = []
    es_sentences_all = []
    size = len(entries)
    i = 0
    for entry in entries:
        mono_agr, agr_sentences, es_sentences = process_meaning(entry.word, entry.meaning, entry.grammatical_category)

        mono_agr_all.extend(mono_agr)
        agr_sentences_all.extend(agr_sentences)
        es_sentences_all.extend(es_sentences)
        if (len(agr_sentences) != len(es_sentences)):
            print(f'{i}/{size} - {entry.word}')
        i += 1

    return mono_agr_all, agr_sentences_all, es_sentences_all

def add_to_file(text: list[str], output_file: str) -> None:
    """Agrega texto a un archivo especificado.

    Args:
        text (list[str]): Lista de oraciones a escribir en el archivo.
        output_file (str): Ruta del archivo de salida.
    """
    with open(output_file, 'a', encoding='utf-8') as file:
        for sentence in text:
            file.write(sentence + '\n')

page_ranges = {
    'a': (8, 46),
    'b': (47, 57),
    'ch': (59, 65),
    'd': (67, 77),
    'e': (79, 86),
    'i': (88, 100),
    'j': (102, 109),
    'k': (111, 126),
    'm': (128, 132),
    'n': (134, 140),
    'p': (142, 152),
    's': (154, 159),
    'sh': (161, 164),
    't': (166, 177),
    'ts': (179, 185),
    'u': (187, 196),
    'w': (198, 208),
    'y': (210, 218),
}

def main():
    pdf_path = get_file_path('../../data/pdf/1. Diccionario-Awajun-Castellano.pdf')

    print(f"Looking for PDF at: {pdf_path}")

    if not os.path.isfile(pdf_path):
        print(f"Error: The file {pdf_path} does not exist")
    else:
        print("File found. Proceeding with extraction...")
        # file_mono_agr_path = get_file_path('../../data/raw/1_Diccionario Awajun-es.agr')
        file_agr_path = get_file_path('../../data/raw/1_Diccionario Awajun-Castellano.agr')
        file_es_path = get_file_path('../../data/raw/1_Diccionario Awajun-Castellano.es')
        
        reader = pypdf.PdfReader(pdf_path)

        # Extract pages dynamically
        extracted_pages = {}
        for key, (start, end) in page_ranges.items():
            extracted_pages[key] = extract_pages(reader, start, end)

        # Remove prefix phrases and last line letter from each extracted page
        cleaned_pages = {}
        for key, pages in extracted_pages.items():
            cleaned_pages[key] = remove_prefix_phrases_and_last_line(pages)
        
        # Process each dictionary to generate multiple entries
        processed_dictionaries = {}
        for key, cleaned in cleaned_pages.items():
            processed_dictionaries[key] = process_dictionary_entries(cleaned)

        for key, dictionary in processed_dictionaries.items():
            mono_agr, agr_sentences, es_sentences = process_multiple_entries(dictionary)
            # add_to_file(mono_agr, file_mono_agr_path)
            add_to_file(agr_sentences, file_agr_path)
            add_to_file(es_sentences, file_es_path)

        print("Extraction finished.")
        print(f"The agr file can be found at {file_agr_path}")
        print(f"The es file can be found at {file_es_path}")

if __name__ == "__main__":
    main()