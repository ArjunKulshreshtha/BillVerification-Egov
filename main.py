import textwrap
import google.generativeai as genai

genai.configure(api_key="AIzaSyAFTkGfybl1srXjb6Z-qZWsnDT1ADdL83E")


# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)


import PIL.Image

img = PIL.Image.open('handwriting.jpg')

model = genai.GenerativeModel('gemini-pro-vision')

response = model.generate_content(img)

response = model.generate_content(["Convert all text in this image to JSON format", img], stream=True)
response.resolve()

print(response.text)




