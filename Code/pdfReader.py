import os
import time
import fitz

def pdf_to_images(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Create a directory to save the images
    output_dir = os.path.dirname(pdf_path)
    # output_dir = os.path.join(output_dir, 'pdf_images')
    # os.makedirs(output_dir, exist_ok=True)

    # Iterate over each page in the PDF
    for i in range(len(doc)):
        # Render the page as an image
        page = doc.load_page(i)
        pix = page.get_pixmap()

        # Save the image to the output directory
        image_path = os.path.join(output_dir, f'{time.time}_page_{i+1}.jpg')
        pix.save(image_path, 'JPEG')

    print(f'PDF converted to images. Saved to: {output_dir}')

# Example usage
pdf_path = '/path/to/your/pdf.pdf'
pdf_to_images(pdf_path)