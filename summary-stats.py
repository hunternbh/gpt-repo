#################################### Check number of unique companies ###################################################################
# import pandas as pd
# import os

# def count_unique_values_in_column(file_path, column_name):
#     # Check if the file exists
#     if not os.path.isfile(file_path):
#         raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
#     # Read the CSV
#     df = pd.read_csv(file_path)

#     if column_name not in df.columns:
#         raise ValueError(f"Column '{column_name}' does not exist in the file.")

#     # Count unique values in the specified column
#     return df[column_name].nunique()

# # Example usage
# file_name = r"C:\Users\hia_n\Desktop\ghost-jobs2\data\combined_interview_reviews.csv"
# column_name = "folder_name"

# unique_count = count_unique_values_in_column(file_name, column_name)
# print(f"Number of unique values in '{column_name}': {unique_count}")

#1200

#################################### Check number of dates ###################################################################
# import pandas as pd
# import os

# def analyze_dates(file_path, date_column):
#     # Check if the file exists
#     if not os.path.isfile(file_path):
#         raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
#     # Read the CSV
#     df = pd.read_csv(file_path)

#     if date_column not in df.columns:
#         raise ValueError(f"Column '{date_column}' does not exist in the file.")
    
#     # Convert to datetime
#     df[date_column] = pd.to_datetime(df[date_column], errors='coerce')

#     # Drop invalid dates
#     df = df.dropna(subset=[date_column])

#     # Extract year counts
#     year_counts = df[date_column].dt.year.value_counts().sort_index()

#     # Get earliest and latest date
#     earliest_date = df[date_column].min()
#     latest_date = df[date_column].max()

#     return year_counts, earliest_date, latest_date

# # Example usage
# file_path = r"C:\Users\hia_n\Desktop\ghost-jobs2\data\combined_interview_reviews.csv"
# date_column = "date"

# year_counts, earliest, latest = analyze_dates(file_path, date_column)

# print("Number of dates per year:")
# print(year_counts)
# print(f"\nEarliest date: {earliest.date()}")
# print(f"Latest date: {latest.date()}")

# Number of dates per year:
# date
# 2009      437
# 2010     1626
# 2011     1764
# 2012     3840
# 2013     5804
# 2014     8870
# 2015    16532
# 2016    16787
# 2017    18184
# 2018    16319
# 2019    17499
# 2020    15439
# 2021    31451
# 2022    38218
# 2023    50239
# 2024    41370
# Name: count, dtype: int64

# Earliest date: 2009-03-11
# Latest date: 2024-07-16

#################################### Eliminate less then 10, and noname ###################################################################

# import pandas as pd

# def clean_folder_names(file_path, column_name='folder_name', min_count=10):
#     # Load CSV
#     df = pd.read_csv(file_path)
#     original_count = len(df)

#     # Remove rows where folder_name == "(no)name"
#     df = df[df[column_name] != "(no)name"]

#     # Remove rows where folder_name occurs < min_count times
#     value_counts = df[column_name].value_counts()
#     valid_folders = value_counts[value_counts >= min_count].index
#     df = df[df[column_name].isin(valid_folders)]

#     # Calculate removed rows
#     final_count = len(df)
#     removed_count = original_count - final_count
#     print(f"Rows removed: {removed_count}")

#     # Overwrite original file
#     df.to_csv(file_path, index=False)
#     print(f"Cleaned data saved to: {file_path}")

# # Example usage
# file_path = r"C:\Users\hia_n\Desktop\ghost-jobs2\data\combined_interview_reviews.csv"
# clean_folder_names(file_path)

# Rows removed: 85

import os

from config import OPENAI_API_KEY  # Import from config.py
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

from openai import OpenAI
import pandas as pd
import time
# Initialize OpenAI client (make sure your OPENAI_API_KEY is set)
client = OpenAI()

# Few-shot examples to guide the model
few_shot_prompt = """
You are a helpful assistant that classifies interview reviews as "Ghost" or "Real".

# Instructions
* Only respond with "Ghost" or "Real".
* A "Ghost" job means the interview was conducted, but the job does exist, or that employers are not planning to fill immediately.
* A "Real" job means the interview was conducted for an actual position that the company intended to fill.

# Examples

<interview_review id="example-1">
Had a great chat with the team, but after that, nothing. They keep the job posting up, but I suspect it was just to gather candidates.</interview_review>
<assistant_response id="example-1">
Ghost
</assistant_response>

<interview_review id="example-2">
I interviewed with two team members and received an offer the next week. Everything was smooth and professional.
</interview_review>
<assistant_response id="example-2">
Real
</assistant_response>

<interview_review id="example-3">
They kept interviewing candidates for months, and I found out from an employee the position was not hiring all along.
</interview_review>
<assistant_response id="example-3">
Ghost
</assistant_response>
"""

def classify_review(review_text):
    review_block = f"<interview_review id=\"user\">\n{review_text}\n</interview_review>"
    messages = [
        {"role": "system", "content": "You are a helpful assistant that classifies interview reviews as Ghost or Real."},
        {"role": "user", "content": few_shot_prompt + review_block}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error classifying review: {e}")
        return "Error"

def process_csv(file_path, review_column="interview", output_column="gpt"):
    df = pd.read_csv(file_path)

    # Only classify reviews that haven't been classified yet (optional)
    if output_column in df.columns:
        mask = df[output_column].isna()
    else:
        df[output_column] = ""
        mask = [True] * len(df)

    for idx in df[mask].index:
        review = df.at[idx, review_column]
        if pd.notna(review) and review.strip():
            df.at[idx, output_column] = classify_review(review)
            time.sleep(0.1)  # Add slight delay to avoid rate limits

    df.to_csv(file_path, index=False)
    print(f"Classification completed. File saved to: {file_path}")

# Example usage
file_path = r"C:\Users\hia_n\Desktop\test.csv"
process_csv(file_path)