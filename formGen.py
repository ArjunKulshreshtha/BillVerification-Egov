import gptAI

# Load the image
image_path = "imgs/formGen.jpg"

# Convert the image to text using GPT AI
text = gptAI.generate_text_from_image_gpt("Generate an HTML form based on the given image. Do not populate values. At the press of the submit button it should call an API and send the data to it.", image_path)
# text = text.replace("\n", "<br>")
# text = text[8:]
# text = text[:-4]
# Put text in an HTML file
with open("form.html", "w") as f:
    f.write(text)