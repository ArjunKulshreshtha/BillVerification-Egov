from openai import OpenAI

client = OpenAI(api_key='sk-proj-XC0h775mWvBgQ5gVxPUkT3BlbkFJhFAUtP6JiUFaTplHo68s')
import base64

# Set up your OpenAI API key

# Function to send image and text prompt to GPT-4o
def generate_text_from_image(text_prompt):
    # Generate text from image and prompt using GPT-4o
    with open('testing.jpg', 'rb') as image_file:
        image_data = image_file.read()

    image_base64 = base64.b64encode(image_data).decode('utf-8')

    response = client.completions.create(model='gpt-4o',
    prompt=f"Image: {image_base64}\nText prompt: {text_prompt}",
    max_tokens=100,
    temperature=0.7,
    n=1,
    stop=None)

    # Extract the generated text from the response
    generated_text = response.choices[0].text.strip()

    return generated_text

# Example usage
text_prompt = 'Extract text from this image'

generated_text = generate_text_from_image(text_prompt)
print(generated_text)