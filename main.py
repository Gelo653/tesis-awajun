import argparse
import os
from src.data.Data_Extraction import run_all_extractions
from src.data.Data_Processing import process_data
from src.visualization.Data_visualization import tsv_from_file

def main():
    parser = argparse.ArgumentParser(description="Proyect for translator implementation.")

    parser.add_argument(
        '-e', '--extract',
        action='store_true',
        help="Run data extraction process"
    )

    parser.add_argument(
        '-p', '--process',
        action='store_true',
        help='Process data'
    )

    parser.add_argument(
        '-c', '--count',
        action='store_true',
        help="Count words and transform it on a tsv file."
    )

    args = parser.parse_args()

    if args.extract:
        print("Running data extraction...")
        output_directory = 'data/raw'
        run_all_extractions(output_directory)
    elif args.process:
        print("Processing data...")
        process_data()
    elif args.count:
        print("Counting words")
        tsv_from_file()
    else:
        print("No action specified. Use -e or --extract to run data extraction")


if __name__ == "__main__":
    main()
