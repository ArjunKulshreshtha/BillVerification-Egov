# Make sure to trim excel sheet to only include the columns you want to extract
# This script reads an Excel file and extracts specific columns to create a list of dictionaries that can be converted to JSON.


import os
import pandas as pd
import json
from datetime import datetime

def convert_datetime_to_string(obj):
    """Recursively convert datetime objects to strings in the dictionary."""
    if isinstance(obj, dict):
        return {k: convert_datetime_to_string(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetime_to_string(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return obj

def populateSchemaFromExcel(excel_file_path, input_json_path):

    # Load the input JSON file to get the keys
    with open(input_json_path, 'r') as json_file:
        input_json = json.load(json_file)
    required_keys = set(input_json.keys())

    # Print the keys of the input JSON
    print("Keys from the input JSON file:")
    print(required_keys)

    # Read the Excel file to inspect the actual column names
    df = pd.read_excel(excel_file_path)
    print("Actual columns in the Excel file:")
    print(df.columns.tolist())

    # Filter the DataFrame to include only the relevant columns
    # (columns that match the keys of the input JSON)
    columns_to_extract = [col for col in df.columns if col in required_keys]

    # Read the Excel file again, selecting only the relevant columns
    df = pd.read_excel(excel_file_path, usecols=columns_to_extract)

    # Filter out rows that are not needed (if any specific condition is given)
    # For example, if you want to filter out rows where any of the specified columns are NaN
    df = df.dropna(subset=columns_to_extract)

    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')

    data = [convert_datetime_to_string(record) for record in data]

    # Print the JSON objects
    for record in data:
        print(record)

    # Save the filtered data to a JSON file
    json_output_path = os.path.join(os.path.dirname(excel_file_path), 'data_filtered.json')
    with open(json_output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


if __name__ == '__main__':
    # Example usage
    excel_file_path = './Dataset_Filtered/Data1/Feb and March month Reimbursement bill.xlsx'
    input_json_path = './Schema/sample.json'

    populateSchemaFromExcel(excel_file_path, input_json_path)
