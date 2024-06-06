# Make sure to trim excel sheet to only include the columns you want to extract
# This script reads an Excel file and extracts specific columns to create a list of dictionaries that can be converted to JSON.


def populateSchemaFromExcel(excel_file_path):

    import os
    import pandas as pd
    import json

    # Define the path to your Excel file
    # excel_file_path = '.\Dataset_Filtered\Data1\Feb and March month Reimbursement bill.xlsx'

    df = pd.read_excel(excel_file_path)

    # Print the actual column names to adjust the columns_to_extract list
    print("Actual columns in the Excel file:")
    print(df.columns.tolist())

    # Define the columns you want to extract (adjust these based on the actual column names)
    columns_to_extract = ['Expense Type', 'Purpose', 'Mission', 'Category', 'Date', 'From', 'To', 'Amount ', 'Links']

    # Read the Excel file again, selecting only the relevant columns
    df = pd.read_excel(excel_file_path, usecols=columns_to_extract)

    # Filter out rows that are not needed (if any specific condition is given)
    # For example, if you want to filter out rows where any of the specified columns are NaN
    df = df.dropna(subset=columns_to_extract)

    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')

    # Print the JSON objects
    for record in data:
        print(record)

    # Optional: Save to a JSON file
    json_output_path = os.path.dirname(excel_file_path) + '/data_raw.json'
    with open(json_output_path, 'w') as json_file:
        json.dump(str(data), json_file, indent=4)