import json
import pandas as pd
import os

def calculate_match_score(json1, json2):
    """Calculate the match score based on matching elements in the two JSON objects."""
    if json1 == json2:
        return 100, "yes"

    json1_flat = flatten_json(json1)
    json2_flat = flatten_json(json2)

    matches = 0
    for key in json1_flat:
        if key in json2_flat and json1_flat[key] == json2_flat[key]:
            matches += 1

    total_elements = max(len(json1_flat), len(json2_flat))
    match_score = (matches / total_elements) * 100 if total_elements > 0 else 0
    match = "yes" if match_score > 0 else "no"
    return match_score, match

def flatten_json(y):
    """Flatten a nested JSON object."""
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '_')
        elif isinstance(x, list):
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def log_to_excel(file_path, json_path1, json_path2, match_score, match):
    """Log the details into an Excel file."""
    data = {
        'File Path': [file_path],
        'JSON Path 1': [json_path1],
        'JSON Path 2': [json_path2],
        'Match Score': [match_score],
        'Match': [match]
    }

    df = pd.DataFrame(data)
    excel_path = file_path

    if os.path.exists(excel_path):
        existing_df = pd.read_excel(excel_path)
        new_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        new_df = df

    new_df.to_excel(excel_path, index=False)

def compare_json_files_and_log(file_path, json_path1, json_path2):
    """Compare two JSON files and log the results into an Excel file."""
    with open(json_path1, 'r') as file1, open(json_path2, 'r') as file2:
        json1 = json.load(file1)
        json2 = json.load(file2)

    match_score, match = calculate_match_score(json1, json2)
    log_to_excel(file_path, json_path1, json_path2, match_score, match)

# Example usage:
compare_json_files_and_log('comparison_log.xlsx', 'sample.json', 'sample2.json')
