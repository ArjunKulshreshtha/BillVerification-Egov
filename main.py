import openai
import os   

os.environ['OPENAI_API_KEY'] = "sk-proj-XC0h775mWvBgQ5gVxPUkT3BlbkFJhFAUtP6JiUFaTplHo68s" # Replace with your API Key
openai.api_key = os.getenv("OPENAI_API_KEY")


def chatGPT_image(prompt, 
            image_url,
            model="gpt-4o",
            detail = "low",
            max_tokens=300):
    error_message = ""
    try:
        messages = [{
            'role': 'user', 'content': [
            {"type": "text", "text": prompt},
            {"type": "image_url",
             "image_url": {"url" : image_url, "detail" : detail},
             },
            ],
            }]

        response = openai.ChatCompletion.create(
          model = model,
          messages = messages,
          max_tokens=max_tokens
        )
        
    except Exception as e:
        error_message = str(e)

    if error_message:
        return "An error occurred: {}".format(error_message)
    else:
        return response['choices'][0]['message']['content']

# Run Function    
response = chatGPT_image(prompt = "What's in the image?",
              image_url = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgCGchJj9jVRP0jMND1a6tJXj7RcYWtnCO4J6YcbPTXrNxiCvs_3NSk7h2gB0h2sc_6bTvwPrBeBHwUA45AXAhaw1uuINuPDcHCbARxpgJIXM5Spi_0P45aR6tqZ_yof-YlNn41LhzHjfW-wsV3mhxBug4To8xtgyMzsHLbm3XoaHZmYUdNY1YWJA5rh6cB/s1600/Soccer-1490541_960_720.jpg")

print(response)