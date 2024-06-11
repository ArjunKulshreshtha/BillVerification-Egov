import json
import pandas as pd
import os
from collections import Counter

def flatten_json(y, parent_key='', sep='.'):
    """Flatten a nested JSON object, including lists."""
    items = []
    if isinstance(y, dict):
        for k, v in y.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.extend(flatten_json(v, new_key, sep=sep).items())
    elif isinstance(y, list):
        for i, v in enumerate(y):
            new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
            items.extend(flatten_json(v, new_key, sep=sep).items())
    else:
        items.append((parent_key, y))
    return dict(items)

def calculate_match_score(json1, json2):
    """Calculate the match score based on matching elements in the two JSON objects."""
    json1_flat = flatten_json(json1)
    json2_flat = flatten_json(json2)

    matches = 0
    total_weight = 0

    all_keys = set(json1_flat.keys()).union(set(json2_flat.keys()))

    for key in all_keys:
        value1 = json1_flat.get(key, None)
        value2 = json2_flat.get(key, None)

        if value1 == value2:
            matches += 1
        elif value1 is not None and value2 is not None:
            matches += calculate_partial_score(value1, value2)
        
        total_weight += 1

    match_score = (matches / total_weight) * 100 if total_weight > 0 else 0
    match = "yes" if match_score > 0 else "no"
    return match_score, match

def calculate_partial_score(value1, value2):
    """Calculate a partial match score between two values."""
    if value1 == "N/A" or value2 == "N/A":
        return 0  # Skip "N/A" values
    if isinstance(value1, str) and isinstance(value2, str):
        # Ratio of common characters
        common_chars = len(set(value1) & set(value2))
        return common_chars / max(len(value1), len(value2))
    elif isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
        # Inverse of the relative difference
        return 1 - abs(value1 - value2) / max(abs(value1), abs(value2))
    elif isinstance(value1, list) and isinstance(value2, list):
        # Use Counter to account for duplicates
        counter1 = Counter(value1)
        counter2 = Counter(value2)
        common_elements = sum((counter1 & counter2).values())
        total_elements = sum(counter1.values())
        return common_elements / total_elements if total_elements > 0 else 0
    return 0


def remove_duplicates(lst):
    """Remove duplicate dictionaries from a list."""
    seen = set()
    new_lst = []
    for d in lst:
        if isinstance(d, dict):
            # Convert dictionary to a frozenset of its items
            dict_as_frozenset = frozenset(d.items())
            if dict_as_frozenset not in seen:
                seen.add(dict_as_frozenset)
                new_lst.append(d)
        else:
            new_lst.append(d)
    return new_lst

def log_to_excel(file_path, json_path1, json_path2, match_score, match):
    """Log the details into an Excel file."""
    data = {
        'File Path': [file_path],
        'JSON Path 1': [json_path1],
        'JSON Path 2': [json_path2],
        'Match Score': [match_score],
        'Match': [match]
    }

    print(match_score)


    df = pd.DataFrame(data)
    excel_path = file_path

    # Extract the directory from the file path
    dir_name = os.path.dirname(excel_path)
    print(excel_path)

    # If the directory does not exist, create it
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    if os.path.exists(excel_path):
        existing_df = pd.read_excel(excel_path)
        new_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        new_df = df

    new_df.to_excel(excel_path, index=False)

def compare_json_files_and_log(file_path, json_path1, json_path2):
    """Compare two JSON files and log the results into an Excel file."""
    try:
        with open(json_path1, 'r') as file1, open(json_path2, 'r') as file2:
            json1 = remove_duplicates(json.load(file1))
            json2 = remove_duplicates(json.load(file2))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return

    match_score, match = calculate_match_score(json1, json2)
    log_to_excel(file_path, json_path1, json_path2, match_score, match)

# Example usage:

if __name__ == '__main__':
    compare_json_files_and_log('C:\\Users\\arjun\\Documents\\egovs\\DocumentVerification\\testing\\ExperimentalTesting\\comparison_log.xlsx', 'sample.json', 'sample2.json')  # noqa: E999
