import os
import pandas as pd
import argparse


def count_unique_values_in_column(file_path: str, column_name: str) -> int:
    """Return the number of unique values in a CSV column."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    df = pd.read_csv(file_path)

    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the file.")

    return df[column_name].nunique()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count unique values in a column")
    parser.add_argument("file_path", help="Path to the CSV file")
    parser.add_argument("column_name", help="Name of the column to analyze")
    args = parser.parse_args()
    result = count_unique_values_in_column(args.file_path, args.column_name)
    print(f"Number of unique values in '{args.column_name}': {result}")
