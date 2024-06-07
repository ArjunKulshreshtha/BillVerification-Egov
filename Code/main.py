import json
import shutil
import cv2filters
import gemini
import gpt4o
import logData
import pdfReader
import populateSchemaExcel

import os


dirs = []

text_prompt = '''
    Extract all text from this image.
    Use the text from this image to populate the following JSON object with data.
    Output just the json object and nothing else.
    Ensure that all fields are populated correctly. Do not add fields that are not present in the image or in the JSON object.
    Ensure that the data types are correct.
    Any fields for which the data type cannot be determined should be left as strings.
    Any fields for which the data cannot be found in the image should be marked as "N/A".
    Ensure that there are no additional characters so that output can be easily converted to JSON

    The format for the JSON object is as follows
    {
    "Date": "yyyy-mm-dd",
    "Amount ": 0
  }

    An example of an acceptable output is:
    {
    "Date": "2023-06-05",
    "Amount ": 250.75
  }

  An example of an unnacceptable output is:
    {
        "Date": "June 5, 2023",
        "Amount ": "Two hundred and fifty dollars and seventy-five cents"
    }

    or

    ```{
    "Date": "2023-06-05",
    "Amount ": 250.75
  }```

'''

def list_dirs(directory_path):
    """List all files in the specified directory."""
    try:
        # Iterate over all the files in the directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            # if os.path.isfile(file_path):
            #     print(f"File: {file_path}")
            if os.path.isdir(file_path):
                # print(f"Directory: {file_path}")
                dirs.append(file_path)
                # If you want to recursively list files in subdirectories, uncomment the following line:
                # list_files_in_directory(file_path)
    except Exception as e:
        print(f"An error occurred: {e}")



def list_excel_files(directory_path):
    """Print the names of all Excel files in the specified directory."""
    try:
        # Iterate over all the files in the directory
        for filename in os.listdir(directory_path):
            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                return os.path.join(directory_path, filename)
    except Exception as e:
        print(f"An error occurred: {e}")


def move_images_to_subdirectory(directory_path):
    """Move all images in the directory to a sub-directory labelled 'images'."""
    # List of common image file extensions
    image_extensions = ('.jpg', '.jpeg', '.png')
    
    # Path to the sub-directory
    images_subdirectory = os.path.join(directory_path, 'imgs')
    
    # Create the sub-directory if it does not exist
    if not os.path.exists(images_subdirectory):
        os.makedirs(images_subdirectory)
    
    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(image_extensions):
            # Move the file to the sub-directory
            shutil.move(file_path, images_subdirectory)
            print(f"Moved: {filename}")

def extract_json(s):
    """Extract the content between the first opening curly brace and the last closing curly brace."""
    try:
        # Find the first opening curly brace
        start = s.index('{')
        # Find the last closing curly brace
        end = s.rindex('}') + 1
        # Extract the content between the braces
        content = s[start:end]
        return content
    except ValueError:
        # Return an empty string if braces are not found
        return ""

def save_dict_to_json_file(string_data, output_file_path):
    """
    Append a string representation of a JSON object to an existing JSON file.

    :param string_data: String representation of a JSON object
    :param output_file_path: Path to the output JSON file
    """
    try:
        # Convert string to JSON object
        new_data = json.loads(string_data)
        
        # Read existing data from the file, if it exists
        try:
            with open(output_file_path, 'r') as json_file:
                existing_data = json.load(json_file)
        except FileNotFoundError:
            # If file does not exist, start with an empty list
            existing_data = []

        # Append new data to existing data
        if isinstance(existing_data, list):
            existing_data.append(new_data)
        else:
            raise ValueError("The existing JSON data is not a list. Cannot append.")

        # Write updated data back to the file
        with open(output_file_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)
        print(f"Data successfully appended to {output_file_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


directory_path = 'C:\\Users\\arjun\\Documents\\egovs\\DocumentVerification\\testing\\ExperimentalTesting\\Dataset_Filtered'  # Replace with your directory path
list_dirs(directory_path)




# Loop through all directories
for directory in dirs:


    # Populating json from excel
    data_source = list_excel_files(directory)
    if data_source:
        populateSchemaExcel.populateSchemaFromExcel(data_source, 'schema/sample.json')
    else:
        print(f"No Excel files found in directory: {directory}")


    bill_path = os.path.join(directory, "Bills")

    # Move images to subdirectory
    move_images_to_subdirectory(bill_path)

    # Test Cases

    # run pdfReader.pdf_to_images on every pdf in the directory
    # Loop through every PDF in the directory
    for filename in os.listdir(bill_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(bill_path, filename)
            print(f"Processing PDF: {pdf_path}")
            pdfReader.pdf_to_images(pdf_path)

    # Loop through every image in the imgs sub-directory
    for filename in os.listdir(os.path.join(bill_path, 'imgs')):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            image_path = os.path.join(bill_path, 'imgs', filename)
            
            
            #? Run test cases

            # Test Case 1: Gpt-4o with unfiltered image
            save_dict_to_json_file(gpt4o.generate_text_from_image_gpt(text_prompt, image_path), os.path.join(directory, 'output_gpt_raw.json'))

            # # Test Case 2: Gemini with unfiltered image
            save_dict_to_json_file(gemini.generate_text_from_image_gemini(text_prompt, image_path), os.path.join(directory, 'output_gemini_raw.json'))

            # # Test Case 3: Gpt-4o with grayscale image
            save_dict_to_json_file(gpt4o.generate_text_from_image_gpt(text_prompt, cv2filters.convert_to_grayscale(image_path)), os.path.join(directory, 'output_gpt_grayscale.json'))

            # # Test Case 4: Gemini with grayscale image
            save_dict_to_json_file(gemini.generate_text_from_image_gemini(text_prompt, cv2filters.convert_to_grayscale(image_path)), os.path.join(directory, 'output_gemini_grayscale.json'))

            # # Test Case 5: Gpt-4o with binary image            
            save_dict_to_json_file(gpt4o.generate_text_from_image_gpt(text_prompt, cv2filters.apply_threshold(image_path, 160)), os.path.join(directory, 'output_gpt_binary.json'))

            # # Test Case 6: Gemini with binary image
            save_dict_to_json_file(gemini.generate_text_from_image_gemini(text_prompt, cv2filters.apply_threshold(image_path, 160)), os.path.join(directory, 'output_gemini_binary.json'))

            # # Test Case 7: Gpt-4o with processed image
            save_dict_to_json_file(gpt4o.generate_text_from_image_gpt(text_prompt, cv2filters.process_image(image_path)), os.path.join(directory, 'output_gpt_processed.json'))

            # # Test Case 8: Gemini with processed image
            save_dict_to_json_file(gemini.generate_text_from_image_gemini(text_prompt, cv2filters.process_image(image_path)), os.path.join(directory, 'output_gemini_processed.json'))

    # Log data
    logData.compare_json_files_and_log("./output_data/comparison_log_gpt_raw.xlsx", os.path.join(directory, 'output_gpt_raw.json'), os.path.join(directory, 'data_filtered.json'))
    logData.compare_json_files_and_log("./output_data/comparison_log_gemini_raw.xlsx", os.path.join(directory, 'output_gemini_raw.json'), os.path.join(directory, 'data_filtered.json'))
    logData.compare_json_files_and_log("./output_data/comparison_log_gpt_grayscale.xlsx", os.path.join(directory, 'output_gpt_grayscale.json'), os.path.join(directory, 'data_filtered.json'))
    logData.compare_json_files_and_log("./output_data/comparison_log_gemini_grayscale.xlsx", os.path.join(directory, 'output_gemini_grayscale.json'), os.path.join(directory, 'data_filtered.json'))
    logData.compare_json_files_and_log("./output_data/comparison_log_gpt_binary.xlsx", os.path.join(directory, 'output_gpt_binary.json'), os.path.join(directory, 'data_filtered.json'))
    logData.compare_json_files_and_log("./output_data/comparison_log_gemini_binary.xlsx", os.path.join(directory, 'output_gemini_binary.json'), os.path.join(directory, 'data_filtered.json'))
    logData.compare_json_files_and_log("./output_data/comparison_log_gpt_processed.xlsx", os.path.join(directory, 'output_gpt_processed.json'), os.path.join(directory, 'data_filtered.json'))
    logData.compare_json_files_and_log("./output_data/comparison_log_gemini_processed.xlsx", os.path.join(directory, 'output_gemini_processed.json'), os.path.join(directory, 'data_filtered.json'))


    print("\n--------------------------------\n")