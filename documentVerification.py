#TODO: Implement doc_path validity checking and the PDF to image conversion from main_old.py

import geminiAI
import gptAI
import os
import fitz


field_name = input("Enter the field name: ")
field_value = input("Enter the field value: ")
doc_path = input("Enter the path to the proof: ")


# field_name = "Name"
# field_value = "John Doe"
doc_path = "imgs/" + doc_path


is_pdf = False

if not os.path.exists(doc_path):
    print("Please provide a valid image path")
    exit()

if doc_path.split(".")[-1] in ["pdf"]:
    is_pdf = True
    doc = fitz.open(doc_path)  # open document
    for i, page in enumerate(doc):
        pix = page.get_pixmap()  # render page to an image
        pix.save(f"pdfpics/page_{i+1}.png")

elif doc_path.split(".")[-1] not in ["jpeg", "jpg", "png"]:
    print("That wasnt an image")
    exit()


# Construct the prompt for the AI model using an f-string
text_prompt = f"Extract the field '{field_name}' from the given image, output should be just the value of the field and nothing else"

# Ask which AI model to use
user_choice = input("Enter 'gpt' for GPT-4o or 'gemini' for Gemini AI: ")
if not is_pdf:
    if user_choice == "gpt":
        # Call the function to generate the text from the image using GPT-4o
        response = gptAI.generate_text_from_image_gpt(text_prompt, doc_path)
        print(response)

    elif user_choice == "gemini":
        # Call the function to generate the text from the image using Gemini AI
        response = geminiAI.generate_text_from_image_gemini(text_prompt, doc_path)
        print(response)
else:
    for i in range(1, len(os.listdir("pdfpics"))):
        if user_choice == "gpt":
            response = gptAI.generate_text_from_image_gpt(
                text_prompt, f"pdfpics/page_{i}.png")
            print(response)
        elif user_choice == "gemini":
            response = geminiAI.generate_text_from_image_gemini(
                text_prompt, f"pdfpics/page_{i}.png")
            print(response)

# Call the function to check if the texts match using user input
text_prompt = f"Do '{response}' and '{field_value}' match? Provide a confidence score (out of 100) as well, ensure that a confidence score of 100 is not given unless there is a perfect match"

if user_choice == "gpt":
    response = gptAI.generate_text_from_text_gpt(text_prompt)
    print(response)

elif user_choice == "gemini":
    response = geminiAI.generate_text_from_text_gemini(text_prompt)
    print(response)

# # Call the function to generate the text from the image using Gemini AI
# response = geminiAI.generate_text_from_image_gemini(text_prompt, doc_path)
# print(response.text)

# # Call the function to check if the texts match using geminiAI
# text_prompt = f"Do '{response.text}' and '{field_value}' match? Provide a confidence score (out of 100) as well, ensure that a confidence score of 100 is not given unless there is a perfect match"
# response = geminiAI.generate_text_from_text_gemini(text_prompt)

# print(response.text)