import os
import time
import pandas as pd
import argparse
from openai import OpenAI
from config import OPENAI_API_KEY


os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client = OpenAI()

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


def classify_review(review_text: str) -> str:
    """Classify a single review as Ghost or Real using OpenAI."""
    review_block = f"<interview_review id=\"user\">\n{review_text}\n</interview_review>"
    messages = [
        {"role": "system", "content": "You are a helpful assistant that classifies interview reviews as Ghost or Real."},
        {"role": "user", "content": few_shot_prompt + review_block},
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


def process_csv(file_path: str, review_column: str = "interview", output_column: str = "gpt") -> None:
    """Classify the review column of a CSV and store results in a new column."""
    df = pd.read_csv(file_path)

    if output_column in df.columns:
        mask = df[output_column].isna()
    else:
        df[output_column] = ""
        mask = [True] * len(df)

    for idx in df[mask].index:
        review = df.at[idx, review_column]
        if pd.notna(review) and review.strip():
            df.at[idx, output_column] = classify_review(review)
            time.sleep(0.1)  # Avoid rate limits

    df.to_csv(file_path, index=False)
    print(f"Classification completed. File saved to: {file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify interview reviews")
    parser.add_argument("file_path", help="Path to the CSV file")
    parser.add_argument("--review-column", default="interview", dest="review_column", help="Column containing the review text")
    parser.add_argument("--output-column", default="gpt", dest="output_column", help="Column to store the classification")
    args = parser.parse_args()
    process_csv(args.file_path, args.review_column, args.output_column)
