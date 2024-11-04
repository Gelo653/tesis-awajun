from ..utils.Data_Extraction_functions import extract_lines_from_text, write_lines_to_file, get_file_path
from pypdf import PdfReader
import os
import re

def extract_pages(reader, init, end):
    pages = []
    for i in range(init, end):
        page = reader.pages[i]
        pages.append(page.extract_text())
    return pages

def pages_to_string(pdf_pages):
    text = ''
    for page in pdf_pages:
        text += page
    return text

def main(output_directory: str = 'data/raw'):
    pdf_path = get_file_path('../../data/pdf/8. Paco Yunque.pdf')

    print(f"Looking for PDF at: {pdf_path}")

    if not os.path.isfile(pdf_path):
        print(f"Error: The file {pdf_path} does not exist")
    else:
        print("File found. Proceeding with extraction...")
        reader = PdfReader(pdf_path)

        pages_es = extract_pages(reader, 17, 39)
        pages_agr = extract_pages(reader, 125, 150)

        pages_es = [page.replace('CASTELLANO', '') for page in pages_es]
        pages_es = [page[2:] for page in pages_es]
        pages_es = [page.replace(' -\n', '') for page in pages_es]
        pages_es = [page.replace('- \n', '') for page in pages_es]

        pattern = re.compile(r"AWAJÚN\d+\n")
        pages_agr = [pattern.sub('', page) for page in pages_agr]
        pages_agr = [page.replace(' -\n', '') for page in pages_agr]
        pages_agr = [page.replace('- \n', '') for page in pages_agr]

        text_es = pages_to_string(pages_es)
        text_agr = pages_to_string(pages_agr)

        text_es = text_es.replace(' -', '')
        text_es = text_es.replace('-\n', '')
        text_es = text_es.replace('-\n', '')
        text_agr = text_agr.replace(' -', '')
        text_agr = text_agr.replace('-\n', '')

        lines_es = extract_lines_from_text(text_es)
        lines_agr = extract_lines_from_text(text_agr)

        file_es_path = os.path.join(output_directory,'8_Paco Yunque.es')
        file_agr_path = os.path.join(output_directory, '8_Paco Yunque.agr')

        write_lines_to_file(lines_es, file_es_path)
        write_lines_to_file(lines_agr, file_agr_path)
        print("Extraction finished.")
        print(f"The agr file can be found at {file_agr_path}")
        print(f"The es file can be found at {file_es_path}")

if __name__ == "__main__":
    main()