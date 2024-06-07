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

def extract_json(s):
    """Extract the content between the first opening curly brace and the last closing curly brace."""
    try:
        # Find the first opening curly brace
        start = s.index('{')
        # Find the last closing curly brace
        end = s.rindex('}') + 1
        # Extract the content between the braces
        content = s[start:end]
        return content
    except ValueError:
        # Return an empty string if braces are not found
        return ""

if __name__ == '__main__':
    text_prompt = '''
    Extract all text from this image.
    Use the text from this image to populate the following JSON object with data.
    Output just the json object and nothing else.
    Ensure that all fields are populated correctly. Do not add fields that are not present in the image or in the JSON object.
    Ensure that the data types are correct.
    Any fields for which the data type cannot be determined should be left as strings.
    Any fields for which the data cannot be found in the image should be marked as "N/A".
    Ensure that there are no additional characters so that output can be easily converted to JSON

    The format for the JSON object is as follows
    {
    "Date": "yyyy-mm-dd",
    "Amount ": 0
  }

    An example of an acceptable output is:
    {
    "Date": "2023-06-05",
    "Amount ": 250.75
  }

  An example of an unnacceptable output is:
    {
        "Date": "June 5, 2023",
        "Amount ": "Two hundred and fifty dollars and seventy-five cents"
    }

    or

    ```{
    "Date": "2023-06-05",
    "Amount ": 250.75
  }```

'''
    image_path = ".\Dataset_Filtered\Data1\Bills\imgs\IMG20240309112430.jpg"
    print(extract_json(generate_text_from_image_gemini(text_prompt, image_path)))