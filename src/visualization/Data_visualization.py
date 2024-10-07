from src.visualization.prepare_tsv import count_words_in_file

def tsv_from_file():
    agr_input = "./data/processed/agr_corpus.agr"
    agr_output = "./data/processed/agr_corpus.tsv"

    esp_input = "./data/processed/esp_corpus.es"
    esp_output = "./data/processed/esp_corpus.tsv"

    count_words_in_file(agr_input, agr_output)
    count_words_in_file(esp_input, esp_output)

if __name__ == "__main__":
    tsv_from_file()