import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


genai.configure(api_key="AIzaSyAFTkGfybl1srXjb6Z-qZWsnDT1ADdL83E")


for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)


import PIL.Image

img = PIL.Image.open('testing.jpg')

model = genai.GenerativeModel('gemini-pro-vision')

response = model.generate_content(img)

to_markdown(response.text)


response = model.generate_content(["Convert all text in this image to JSON format", img], stream=True)
response.resolve()

print(response.text)




