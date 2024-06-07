import constants
import base64
import requests


#TODO: Provide list of categories in text prompt


def generate_text_from_image_gpt(text_prompt, image_path):
    # OpenAI API Key
    api_key = constants.openai_api_key

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')


    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4o",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": text_prompt
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 600
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    return (response.json().get("choices")[0]["message"]["content"])



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
    print(generate_text_from_image_gpt(text_prompt, image_path))