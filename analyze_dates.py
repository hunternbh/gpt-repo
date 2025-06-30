import os
import pandas as pd
import argparse
from typing import Tuple


def analyze_dates(file_path: str, date_column: str) -> Tuple[pd.Series, pd.Timestamp, pd.Timestamp]:
    """Return counts per year and the earliest and latest dates."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    df = pd.read_csv(file_path)

    if date_column not in df.columns:
        raise ValueError(f"Column '{date_column}' does not exist in the file.")

    df[date_column] = pd.to_datetime(df[date_column], errors="coerce")
    df = df.dropna(subset=[date_column])

    year_counts = df[date_column].dt.year.value_counts().sort_index()
    earliest_date = df[date_column].min()
    latest_date = df[date_column].max()

    return year_counts, earliest_date, latest_date


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze a date column")
    parser.add_argument("file_path", help="Path to the CSV file")
    parser.add_argument("date_column", help="Name of the date column")
    args = parser.parse_args()
    years, earliest, latest = analyze_dates(args.file_path, args.date_column)
    print("Number of dates per year:")
    print(years)
    print(f"Earliest date: {earliest.date()}")
    print(f"Latest date: {latest.date()}")
