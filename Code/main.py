import shutil
import cv2filters
import gemini
import gpt4o
import logData
import pdfReader
import populateSchemaExcel

import os


dirs = []

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
            image_path = os.path.join(directory, 'imgs', filename)
            print(f"Processing image: {image_path}")



    print("\n--------------------------------\n")