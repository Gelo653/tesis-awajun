import camelot
import numpy as np
import pandas as pd
import re
import os

from ..utils.Data_Extraction_functions import get_file_path

pd.set_option('future.no_silent_downcasting', True)

def extract_tables_from_pdf(pdf_path, output_es_path, output_agr_path):
    """
    Extrae tablas de un archivo PDF y guarda los datos en dos archivos de texto separados.
    
    Args:
        pdf_path (str): Ruta al archivo PDF.
        output_es_path (str): Ruta para guardar el archivo con datos en español.
        output_agr_path (str): Ruta para guardar el archivo con datos en awajun.
    """
    # Cargar tablas desde el PDF
    tables = camelot.read_pdf(pdf_path, pages='13-47')

    tables_df = []
    pattern = re.compile(r'\(?\s*CASTELLANO\s*\)?', re.IGNORECASE)

    for table in tables:
        df = table.df
        df.replace('', np.nan, inplace=True)
        df.replace('\n', '', regex=True, inplace=True)
        df = df.dropna()

        # Eliminar la primera fila si coincide con el patrón
        if not df.empty and pattern.search(df.iloc[0, 0]):
            df = df.drop(df.index[0])

        tables_df.append(df)

    # Escribir datos en los archivos de salida
    with open(output_es_path, 'w', encoding='utf-8') as file_es, open(output_agr_path, 'w', encoding='utf-8') as file_agr:
        for df in tables_df:
            for _, row in df.iterrows():
                file_es.write(f"{row[0]}\n")  # Escribir la columna en el archivo en español
                file_agr.write(f"{row[1]}\n")  # Escribir la columna en el archivo en awajun

    print("Extraction finished.")
    print(f"The agr file can be found at {output_agr_path}")
    print(f"The es file can be found at {output_es_path}")

def main(output_directory: str = 'data/raw'):
    pdf_path = get_file_path('../../data/pdf/2. Guia de comunicación intercultural en salud.pdf')

    print(f"Looking for PDF at: {pdf_path}")

    if not os.path.isfile(pdf_path):
        print(f"Error: The file {pdf_path} does not exist")
    else:
        print("File found. Proceeding with extraction...")
        file_es_path = os.path.join(output_directory,'2_Guia de comunicación intercultural en salud.es')
        file_agr_path = os.path.join(output_directory,'2_Guia de comunicación intercultural en salud.agr')
        extract_tables_from_pdf(pdf_path, file_es_path, file_agr_path)

        print("Extraction finished.")
        print(f"The agr file can be found at {file_agr_path}")
        print(f"The es file can be found at {file_es_path}")

if __name__ == "__main__":
    main()