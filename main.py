import sys
from utils import get_csv_data
from validation import validate_records


def main():
    input_filename = "./data.csv"
    output_filename = "validation_logs.txt"
    sys.stdout = open(output_filename, 'w')  # redirects print statements to output file

    records = get_csv_data(input_filename)

    validate_records(records)


if __name__ == '__main__':
    main()
