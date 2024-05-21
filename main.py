import google.generativeai as genai
import PIL.Image
import os

img_path = 'imgs/PDFTest.pdf'

if not os.path.exists(img_path):
    print("Please provide a valid image path")
    exit()

if img_path.split('.')[-1] in ['pdf']:
    print("That was a PDF")
    exit()

elif img_path.split('.')[-1] not in ['jpeg', 'jpg', 'png']:
    print("That wasnt an image")
    exit()

os.environ["GOOGLE_API_CREDENTIALS"] = "AIzaSyAFTkGfybl1srXjb6Z-qZWsnDT1ADdL83E"
genai.configure(api_key=os.environ.get('GOOGLE_API_CREDENTIALS'))
# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)




img = PIL.Image.open(img_path)

model = genai.GenerativeModel('gemini-pro-vision')

response = model.generate_content(img)

response = model.generate_content(["Convert all text in this image to JSON format. Do not use the rupee symbol. Do nothing except the text extraction.", img], stream=True)

# response = model.generate_content(["Extract and translate to English", img], stream=True)


response.resolve()

print(response)