from bs4 import BeautifulSoup
import requests
import sys
import os
from ..utils.Data_Extraction_functions import extract_lines_from_text, write_lines_to_file, get_file_path

def extract_text_from_url(url, start_phrase, end_phrase):
    """
    Extrae un texto específico de una URL dada.

    Args:
        url (str): La URL desde la cual se extraerá el texto.
        start_phrase (str): La frase que marca el inicio del texto a extraer.
        end_phrase (str): La frase que marca el final del texto a extraer.

    Returns:
        str: El texto extraído si se encontró, de lo contrario None.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()

    start_index = text.find(start_phrase)
    end_index = text.find(end_phrase) + len(end_phrase)

    if start_index != -1 and end_index != -1:
        extracted_text = text[start_index:end_index].replace('\n– ', '\n')
        return extracted_text
    else:
        print("No se pudo encontrar el texto especificado.")
        return None

def main():
    # Extract text in spanish
    url_es = 'https://caaap.org.pe/2017/05/09/carta-de-tarapoto-viii-foro-social-panamazonico/'
    start_phrase_es = "La Panamazonía está"
    end_phrase_es = "la resistencia continúa."

    extracted_text_es = extract_text_from_url(url_es, start_phrase_es, end_phrase_es)

    if extracted_text_es:
        lines_es = extract_lines_from_text(extracted_text_es)
        file_es_path = get_file_path("../../data/raw/16_Carta de Tarapoto.es")
        write_lines_to_file(lines_es, file_es_path)

    # Extract text in awajun
    url_agr = 'https://caaap.org.pe/2017/06/09/la-carta-de-tarapoto-del-viii-fospa-ahora-en-idiomas-awajun-y-wampis/'
    start_phrase_agr = "Panamazoníak initik"
    end_phrase_agr = "juka chichamak wegawai."

    extracted_text_agr = extract_text_from_url(url_agr, start_phrase_agr, end_phrase_agr)
    
    if extracted_text_agr:
        lines_agr = extract_lines_from_text(extracted_text_agr)
        file_agr_path = get_file_path("../../data/raw/16_Carta de Tarapoto.agr")
        write_lines_to_file(lines_agr, file_agr_path)

    print("Extraction finished.")
    print(f"The agr file can be found at {file_agr_path}")
    print(f"The es file can be found at {file_es_path}")


if __name__ == "__main__":
    main()
