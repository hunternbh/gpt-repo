"""Demonstration script showing how to use the refactored modules."""

from classify_reviews import process_csv

# Other steps are implemented in their own modules:
# - unique_companies.py
# - analyze_dates.py
# - clean_data.py

if __name__ == "__main__":
    # Example usage of the classification step
    file_path = r"C:\Users\hia_n\Desktop\test.csv"
    process_csv(file_path)
