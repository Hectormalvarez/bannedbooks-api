# -*- coding: utf-8 -*-
"""pen_america_bannedbooks_scraper

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/111fWNb9zZyuGBbvPanAgKvwFaptpSyJa

updated for script use
"""
import argparse
import datetime
import json
import pandas as pd
from urllib.parse import quote

BANNED_BOOKS_GSHEET_URL = "https://docs.google.com/spreadsheets/d/1hTs_PB7KuTMBtNMESFEGuK-0abzhNxVv4tgpI5-iKe8/edit#gid=1171606318"

SHEET_ID = "1hTs_PB7KuTMBtNMESFEGuK-0abzhNxVv4tgpI5-iKe8"
SHEET_NAME = quote("Sorted by Author & Title")
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", "-o", default="banned_books.json", help="Output file path"
    )
    args = parser.parse_args()

    # Write the list of objects to a JSON file
    with open(args.output, "w") as f:
        json.dump(get_data(), f, indent=4)


def convert_to_objects(df):
    result = []

    # Group the DataFrame by "author" and "title"
    grouped_data = df.groupby(["author", "title"])

    for (author, title), group in grouped_data:
        # Create a dictionary to represent each book
        book_info = {"author": author.lower(), "title": title.lower(), "bans": []}

        # Iterate over each row in the group and create ban objects
        for _, row in group.iterrows():
            ban_object = {}
            for column in df.columns:
                if column not in ["author", "title"]:
                    if not pd.isna(row[column]):
                        ban_object[column.replace(" ", "_")] = str(
                            row[column]
                        ).lower()  # Convert text to lowercase
            book_info["bans"].append(ban_object)

        result.append(book_info)

    return result


def simplify_ban_type(ban_type):
    # Map the simplified values
    ban_mapping = {
        "Banned Pending Investigation": "pending investigation",
        "Banned in Classrooms": "classrooms",
        "Banned in Libraries": "libraries",
        "Banned in Libraries and Classrooms": ("libraries", "classrooms"),
    }

    # Use the mapping to return the simplified ban type
    return ban_mapping.get(ban_type, ban_type)


def extract_month_and_year(df):
    # Custom function to extract month and year from date string
    def extract_date_info(date_str):
        # Split the date string into month and year
        month, year = date_str.split(" ")

        # Convert the month string to a month number
        month_number = datetime.datetime.strptime(month, "%B").month

        return month_number, int(year)

    # Apply the custom function to each row in the "date of challenge/removal" column
    df["month"], df["year"] = zip(
        *df["date of challenge/removal"].apply(extract_date_info)
    )

    # Drop the original "date of challenge/removal" column
    df.drop(columns=["date of challenge/removal"], inplace=True)

    return df


def get_data():
    df = pd.read_csv(url)
    # Get the current third column header
    third_column_header = df.columns[2]
    # Extract the last three words from the header
    last_three_words = " ".join(third_column_header.split()[-3:])
    # Modify the header with the last three words
    df.rename(columns={third_column_header: last_three_words}, inplace=True)
    # Make headers lowercase
    df.columns = df.columns.str.lower()
    # simplify ban column data
    df["type of ban"] = df["type of ban"].apply(simplify_ban_type)
    # split up "date of challenge/removal" column
    # df = extract_month_and_year(df)

    data = convert_to_objects(df)
    return data


if __name__ == "__main__":
    main()
