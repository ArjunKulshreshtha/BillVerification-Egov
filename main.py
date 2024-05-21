import google.generativeai as genai
import PIL.Image
import os
import fitz  

import constants

img_path = 'imgs/pdfTeamAbout.pdf'

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

os.environ["GOOGLE_API_CREDENTIALS"] = constants.api_key
genai.configure(api_key=os.environ.get('GOOGLE_API_CREDENTIALS'))
# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)



if (is_pdf == False):
    img = PIL.Image.open(img_path)
else:
    img = PIL.Image.open("pdfpics/page_1.png")

model = genai.GenerativeModel('gemini-pro-vision')

response = model.generate_content(img)

response = model.generate_content(["Convert all text in this image to JSON format. Do not use the rupee symbol. Do nothing except the text extraction.", img], stream=True)

# response = model.generate_content(["Extract and translate to English", img], stream=True)


response.resolve()

print(response)