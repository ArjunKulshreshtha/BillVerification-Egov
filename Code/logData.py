import json
import pandas as pd
import os

import gpt4o

# Function to calculate match score based on GPT-4's analysis
def calculate_match_score(json1, json2):
    # Convert JSON to text format
    json1_text = json.dumps(json1, indent=2)
    json2_text = json.dumps(json2, indent=2)
    
    prompt = f'Do {json1_text} and {json2_text} match? Provide a confidence score (out of 100) as well, ensure that a confidence score of 100 is not given unless there is a perfect match. Ordering does not matter. Provide only a numerical output and nothing else'

    response = gpt4o.generate_text_from_text_gpt(prompt)
    print("GPT-4 Response:", response)

    # Process GPT-4's response to determine match score
    # matches = 0
    # differences = 0

    # # Assuming GPT-4 response contains lines indicating matches and differences
    # lines = response.splitlines()
    # for line in lines:
    #     if "match" in line:
    #         matches += 1
    #     elif "difference" in line:
    #         differences += 1

    # total_elements = len(json1) + len(json2)
    # match_score = (matches / total_elements) * 100 if total_elements > 0 else 0
    # match = "yes" if match_score > 0 else "no"

    # return match_score, match

# Function to log results to an Excel file
def log_to_excel(file_path, json_path1, json_path2, match_score, match):
    data = {
        'File Path': [file_path],
        'JSON Path 1': [json_path1],
        'JSON Path 2': [json_path2],
        'Match Score': [match_score],
        'Match': [match]
    }

    df = pd.DataFrame(data)
    excel_path = file_path

    dir_name = os.path.dirname(excel_path)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    if os.path.exists(excel_path):
        existing_df = pd.read_excel(excel_path)
        new_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        new_df = df

    new_df.to_excel(excel_path, index=False)

# Main function to compare JSON files and log results
def compare_json_files_and_log(file_path, json_path1, json_path2):
    try:
        with open(json_path1, 'r') as file1, open(json_path2, 'r') as file2:
            json1 = (json.load(file1))
            json2 = (json.load(file2))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return

    match_score, match = calculate_match_score(json1, json2)
    log_to_excel(file_path, json_path1, json_path2, match_score, match)

# Example usage
if __name__ == '__main__':
    compare_json_files_and_log(
        'C:\\Users\\arjun\\Documents\\egovs\\DocumentVerification\\testing\\ExperimentalTesting\\comparison_log.xlsx',
        'sample.json',
        'sample2.json'
    )

