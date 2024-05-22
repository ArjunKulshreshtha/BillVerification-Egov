import google.generativeai as genai
import PIL.Image
import os
import fitz  


img_path = 'imgs/elecbill.jpeg'
text_prompt = 'Extract all text in this file and output it in JSON format. Convert any dates in the file to dd/mm/yyyy format before entering it into the JSON format. Use only ASCII characters. Translate all text to English before putting in JSON format.'

is_pdf = False

if not os.path.exists(img_path):
    print("Please provide a valid image path")
    exit()

if img_path.split('.')[-1] in ['pdf']:
    is_pdf = True
    doc = fitz.open(img_path)  # open document
    for i, page in enumerate(doc):
        pix = page.get_pixmap()  # render page to an image
        pix.save(f"pdfpics/page_{i+1}.png")

elif img_path.split('.')[-1] not in ['jpeg', 'jpg', 'png']:
    print("That wasnt an image")
    exit()


# Let user choose between GPT-4o and Gemini AI
user_choice = input("Enter 'gpt' for GPT-4o or 'gemini' for Gemini AI: ")


if user_choice == 'gpt':
    from gptAI import generate_text_from_image_gpt

    if (is_pdf == False):
        generated_text = generate_text_from_image_gpt(text_prompt, img_path)
        print(generated_text)
    else:
        for i in range(1, len(os.listdir("pdfpics"))):
            generated_text = generate_text_from_image_gpt(text_prompt, f"pdfpics/page_{i}.png")
            print(generated_text)

elif user_choice == 'gemini':
    from geminiAI import generate_text_from_image_gemini

    if (is_pdf == False):
        response = generate_text_from_image_gemini(text_prompt, img_path)
        print(response.text)
    else:
        for i in range(1, len(os.listdir("pdfpics"))):
            response = generate_text_from_image_gemini(text_prompt, f"pdfpics/page_{i}.png")
            print(response.text)

else:
    print("Invalid choice. Please enter 'gpt' or 'gemini'")
    exit()