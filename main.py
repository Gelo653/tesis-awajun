import argparse
from src.data.Data_Extraction import run_all_extractions

def main():
    parser = argparse.ArgumentParser(description="Data extraction script")

    parser.add_argument(
        '-e', '--extract',
        action='store_true',
        help="Run data extraction process"
    )

    args = parser.parse_args()

    if args.extract:
        print("Running data extraction...")
        run_all_extractions()
    else:
        print("No action specified. Use -e or --extract to run data extraction")


if __name__ == "__main__":
    main()
