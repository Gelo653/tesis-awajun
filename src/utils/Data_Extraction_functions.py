import os
import re

def extract_lines_from_text(text):
    """
    Extrae líneas del texto reemplazando ciertos signos de puntuación por saltos de línea.
    
    Args:
        text (str): Texto completo del cual extraer las líneas.
    
    Returns:
    - Lista de líneas extraídas del texto.
    """

    try:
        text = text.replace('\n', '')
        pattern = re.compile(r'([.;:!?])\s*')
        text_with_newlines = pattern.sub(r'\1\n', text)
        lines = text_with_newlines.split('\n')
        lines = [line.strip() for line in lines if line.strip()]
        return lines
    except Exception as e:
        print(f"Error al extraer lineas del texto: {e}")
        return []

def write_lines_to_file(lines, file_path):
    """
    Escribe cada cadena en la lista `lines` en un archivo especificado por `file_path`.
    Cada cadena se escribe en una nueva línea.

    Args:
        lines (list): Lista de cadenas a escribir en el archivo.
        file_path (str): Ruta del archivo donde se escribirán las líneas.
    """

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for line in lines:
                file.write(line + '\n')
    except Exception as e:
        print(f"Error al escribir en el archivo {file_path}: {e}")

def get_file_path(filename):
    """
    Devuelve la ruta absoluta al archivo especificado.

    Args:
        filename (str): El nombre del archivo.

    Returns:
        str: La ruta absoluta al archivo especificado.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
