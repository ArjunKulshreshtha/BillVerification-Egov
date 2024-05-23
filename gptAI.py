import base64
import requests
import constants



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

    return (response.json().get("choices")[0]["message"]["content"])



def generate_text_from_text_gpt(text_prompt):
    # OpenAI API Key
    api_key = constants.openai_api_key

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": text_prompt
            }
        ]
        }
    ],
    "max_tokens": 100
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return (response.json().get("choices")[0]["message"]["content"])



# client = OpenAI(api_key=constants.gpt_api_key   )
# import base64



# # Chatgpt prompt
# #Extract all text in this file and output it in JSON format. Convert any dates in the file to dd/mm/yyyy format before entering it into the JSON format. Use only ASCII characters. Translate all text to English before putting in JSON format.


# # Set up your OpenAI API key

# # Function to send image and text prompt to GPT-4o
# def generate_text_from_image(text_prompt):
#     # Generate text from image and prompt using GPT-4o
#     with open('testing.jpg', 'rb') as image_file:
#         image_data = image_file.read()

#     image_base64 = base64.b64encode(image_data).decode('utf-8')

#     response = client.completions.create(model='gpt-4o',
#     prompt=f"Image: {image_base64}\nText prompt: {text_prompt}",
#     max_tokens=100,
#     temperature=0.7,
#     n=1,
#     stop=None)

#     # Extract the generated text from the response
#     generated_text = response.choices[0].text.strip()

#     return generated_text

# # Example usage
# text_prompt = 'Extract text from this image'

# generated_text = generate_text_from_image(text_prompt)
# print(generated_text)