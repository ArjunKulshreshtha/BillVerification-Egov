import os
import fitz
from flask import Flask, request, jsonify
from flask_cors import CORS
import geminiAI
import gptAI

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

@app.route('/verify_document', methods=['POST'])
def verify_document():
    data = request.json
    
    # Get input data
    field_name = data.get('field_name')
    field_value = data.get('field_value')
    doc_path = data.get('doc_path')
    user_choice = data.get('user_choice')
    
    if not field_name or not field_value or not doc_path or not user_choice:
        return jsonify({"error": "Please provide all required inputs: field_name, field_value, doc_path, user_choice"}), 400
    
    is_pdf = False

    if not os.path.exists(doc_path):
        return jsonify({"error": "Please provide a valid image path"}), 400

    if doc_path.split(".")[-1] in ["pdf"]:
        is_pdf = True
        doc = fitz.open(doc_path)  # open document
        for i, page in enumerate(doc):
            pix = page.get_pixmap()  # render page to an image
            pix.save(f"pdfpics/page_{i+1}.png")

    elif doc_path.split(".")[-1] not in ["jpeg", "jpg", "png"]:
        return jsonify({"error": "The file is not an image"}), 400

    # Construct the prompt for the AI model using an f-string
    text_prompt = f"Extract the field '{field_name}' from the given image, output should be just the value of the field and nothing else"
    responses = []

    if not is_pdf:
        if user_choice == "gpt":
            response = gptAI.generate_text_from_image_gpt(text_prompt, doc_path)
            responses.append(response)
        elif user_choice == "gemini":
            response = geminiAI.generate_text_from_image_gemini(text_prompt, doc_path)
            responses.append(response)
    else:
        for i in range(1, len(os.listdir("pdfpics")) + 1):
            if user_choice == "gpt":
                response = gptAI.generate_text_from_image_gpt(
                    text_prompt, f"pdfpics/page_{i}.png")
                responses.append(response)
            elif user_choice == "gemini":
                response = geminiAI.generate_text_from_image_gemini(
                    text_prompt, f"pdfpics/page_{i}.png")
                responses.append(response)

    # Verify text match
    text_prompt = f"Are '{responses[-1]}' and '{field_value}' the same? Provide a confidence score (out of 100) as well, ensure that a confidence score of 100 is not given unless there is a perfect match. Format the answer as a Yes/No: 'Yes, 95' or 'No, 50'"

    if user_choice == "gpt":
        final_response = gptAI.generate_text_from_text_gpt(text_prompt)
    elif user_choice == "gemini":
        final_response = geminiAI.generate_text_from_text_gemini(text_prompt)

    return jsonify({"extracted_values": responses, "verification_result": final_response})

if __name__ == '__main__':
    app.run(debug=True)
