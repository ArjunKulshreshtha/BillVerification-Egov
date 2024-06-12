import json
import geminiAI
import gptAI

def process_image_with_geminiAI(json_file, image_file):
    # Load JSON object from parameters.json
    with open(json_file) as f:
        json_data = json.load(f)

    # Instructions to populate JSON object
    instructions = "Please populate the following fields in the JSON object. Do not attempt to populate fields that are not present in the image or are not immediately apparent, instead mark with N/A. Do not include any unnecessary information or punctuation. Do not start output with json. Ensure all dates are in the format dd/mm/yyyy. Use only ASCII characters."

    # Text prompt for geminiAI
    text_prompt = f"{json_data}\n{instructions}"

    # Call geminiAI text from image function with image_file and text_prompt
    print(geminiAI.generate_text_from_image_gemini(text_prompt, image_file))

def process_image_with_gptAI(json_file, image_file):
    # Load JSON object from parameters.json
    with open(json_file) as f:
        json_data = json.load(f)

    # Instructions to populate JSON object
    instructions = "Please populate the following fields in the JSON object using the given file, try not to miss any fields. Ensure no details are missed, do not attempt to populate fields that do not have values in the given file. Please do not stop until you have completed the task. Mark any fields you cannot complete with N/A:"

    # instructions = """"""

    # Text prompt for gptAI
    text_prompt = f"{json_data}\n{instructions}"

    # Call gptAI text from image function with image_file and text_prompt
    # Add your code here
    print(gptAI.generate_text_from_image_gpt(text_prompt, image_file))

# Example usage
json_file = "parameters.json"
image_file = "imgs/shopBill.jpg"


# Let user choose between GPT-4o and Gemini AI
user_choice = input("Enter 'gpt' for GPT-4o or 'gemini' for Gemini AI: ")

if user_choice == "gpt":
    process_image_with_gptAI(json_file, image_file)
elif user_choice == "gemini":
    process_image_with_geminiAI(json_file, image_file)
# process_image_with_gptAI(json_file, image_file)