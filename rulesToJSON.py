import os
import fitz
import json

img_path = "imgs/shoppingRules.pdf"
text_prompt = """Make a list of all parameters mentioned in the file. Output the text in JSON format, with the mentioned parameters as the key and the values left blank, ensure individual parameters are seperated and unnecessary punctuation is removed. If no parameter is found, output a blank JSON object, do not output NONE. Make sure that no parameter is missed. This is for the purposes of later populating the values with data from another source. Do not populate the values at this time, only create the JSON format with the keys and blank values. Do not create any data that is not in the file. Use only ASCII characters in the output JSON format. Do not include the word json at the start of the output. Ensure that there will be no issues converting the output directly to JSON, and that the output is not surrounded by quotation marks or backticks. Consider the following example only for formatting, do not copy the example or any parameters from the example. Do not, under any circumstances attempt to populate the values. Do not create seperate, overlapping parameters for validation:

{
    "example_parameter_1": "",
    "example_parameter_2": "",
    "example_parameter_3": "",
    "example_list_of_parameters": {
        "example_sub_parameter_1": {
            "example_sub_sub_parameter_1": "",
        },
        "example_sub_parameter_2": ""
    },
}
"""

is_pdf = False

if not os.path.exists(img_path):
    print("Please provide a valid image path")
    exit()

if img_path.split(".")[-1] in ["pdf"]:
    is_pdf = True
    doc = fitz.open(img_path)  # open document
    for i, page in enumerate(doc):
        pix = page.get_pixmap()  # render page to an image
        pix.save(f"pdfpics/page_{i+1}.png")

elif img_path.split(".")[-1] not in ["jpeg", "jpg", "png"]:
    print("That wasnt an image")
    exit()



def merge_json_objects(json_list):
    merged_dict = {}
    
    for json_str in json_list:
        # Parse each JSON string into a dictionary
        json_dict = json.loads(json_str)
        
        # Merge the dictionary into the final merged dictionary
        merged_dict.update(json_dict)
        
    return json.dumps(merged_dict, indent=4)

# Let user choose between GPT-4o and Gemini AI
user_choice = input("Enter 'gpt' for GPT-4o or 'gemini' for Gemini AI: ")


if user_choice == "gpt":
    from gptAI import generate_text_from_image_gpt

    if not is_pdf:
        generated_text = generate_text_from_image_gpt(text_prompt, img_path)
        print(generated_text)
    else: #I think GPT can do PDFs too
        json_objects = []
        for i in range(1, len(os.listdir("pdfpics"))):
            response = generate_text_from_image_gpt(
                text_prompt, f"pdfpics/page_{i}.png"
            )
            answer = response 
            if (answer is not None):
                json_objects.append(answer)
            # with open('parameters.json', 'w') as f:
            #     json.dump(json_object, f, indent=4)
        json_object = (merge_json_objects(json_objects))
        print(json_object)
        uin = input("Please confirm that this list of parameters is acceptable [Y/n]: ")
        if not uin == "n":
            with open('parameters.json', 'w') as f:
                json.dump(json.loads(json_object), f, indent=4)
            print("The list of parameters has been saved to parameters.json")
        else:
            print("Please re-run the program and try again.")
            exit()

elif user_choice == "gemini":
    from geminiAI import generate_text_from_image_gemini
    # text_prompt = "Extract all text in this file. Translate the text into the English language from whatever language it is in. Make sure to use only ascii characters. Convert all existing dates in the translated text into the dd/mm/yyyy format, do not create dates if the date is blank. Format the translated text into a JSON format, making sure to use the dates in the dd/mm/yyy format. Refrain from doing anything else, under any circumstances do not produce or populate data that is not in the given file."

    if not is_pdf:
        response = generate_text_from_image_gemini(text_prompt, img_path)
        print(response)
    else:
        json_objects = []
        for i in range(1, len(os.listdir("pdfpics"))):
            response = generate_text_from_image_gemini(
                text_prompt, f"pdfpics/page_{i}.png"
            )
            answer = response
            json_objects.append(answer)
            # with open('parameters.json', 'w') as f:
            #     json.dump(json_object, f, indent=4)
        json_object = (merge_json_objects(json_objects))
        print(json_object)
        uin = input("Please confirm that this list of parameters is acceptable [Y/n]: ")
        if not uin == "n":
            with open('parameters.json', 'w') as f:
                json.dump(json.loads(json_object), f, indent=4)
            print("The list of parameters has been saved to parameters.json")
        else:
            print("Please re-run the program and try again.")
            exit()

else:
    print("Invalid choice. Please enter 'gpt' or 'gemini'")
    exit()
