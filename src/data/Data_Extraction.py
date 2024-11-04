import os

import src.data.Paco_Yunque_Data_Extraction as paco_yunque
import src.data.Guia_Comunicacion_Intercultural_Salud_Data_Extraction as guia_intercultaral_salud
import src.data.Carta_Tarapoto_Data_Extraction as carta_tarapoto
import src.data.Diccionario_Awajun_Castellano_Data_Extraction as diccionario_agr_es

def run_all_extractions(output_directory: str):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f'Folder created at: {output_directory}')
    else:
        print(f'Folder already exists at: {output_directory}')
    paco_yunque.main(output_directory)
    guia_intercultaral_salud.main(output_directory)
    carta_tarapoto.main(output_directory)
    diccionario_agr_es.main(output_directory)
    print("Extraction completed without problems.")

if __name__ == "__main__":
    run_all_extractions()