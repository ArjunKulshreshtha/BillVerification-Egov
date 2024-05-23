import google.generativeai as genai
import PIL.Image
import os
import constants


def generate_text_from_image_gemini(text_prompt, img_path):
    os.environ["GOOGLE_API_CREDENTIALS"] = constants.gemini_api_key
    genai.configure(api_key=os.environ.get("GOOGLE_API_CREDENTIALS"))
    img = PIL.Image.open(img_path)
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([repr(text_prompt), img])
    response.resolve()
    return response.text

def generate_text_from_text_gemini(text_prompt):
    os.environ["GOOGLE_API_CREDENTIALS"] = constants.gemini_api_key
    genai.configure(api_key=os.environ.get("GOOGLE_API_CREDENTIALS"))
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([repr(text_prompt)])
    response.resolve()
    return response.text


# Example to generate text
text_prompt = "Extract text"

img_path = "imgs/shopBill.jpg"