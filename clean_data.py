import pandas as pd
import argparse


def clean_folder_names(file_path: str, column_name: str = "folder_name", min_count: int = 10) -> None:
    """Remove infrequent or invalid folder names from the CSV."""
    df = pd.read_csv(file_path)
    original_count = len(df)

    df = df[df[column_name] != "(no)name"]
    value_counts = df[column_name].value_counts()
    valid_folders = value_counts[value_counts >= min_count].index
    df = df[df[column_name].isin(valid_folders)]

    final_count = len(df)
    removed_count = original_count - final_count
    print(f"Rows removed: {removed_count}")

    df.to_csv(file_path, index=False)
    print(f"Cleaned data saved to: {file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean folder names in a CSV")
    parser.add_argument("file_path", help="Path to the CSV file")
    parser.add_argument("--column", default="folder_name", dest="column_name", help="Column to clean")
    parser.add_argument("--min", type=int, default=10, dest="min_count", help="Minimum occurrences to keep")
    args = parser.parse_args()
    clean_folder_names(args.file_path, args.column_name, args.min_count)
