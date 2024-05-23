from PIL import Image

def convert_png_to_jpg(png_filepath, jpg_filepath, quality=95):
  """
  Converts a PNG image to a JPG image with a specified quality.

  Args:
      png_filepath: Path to the PNG image file.
      jpg_filepath: Path to save the converted JPG image file.
      quality: JPG image quality (0-100, higher is better). Defaults to 95.
  """
  try:
    # Open the PNG image
    img = Image.open(png_filepath)

    # Check if the image mode is compatible with JPG (RGBA needs conversion)
    if img.mode == 'RGBA':
      img = img.convert('RGB')

    # Save the image as JPG with specified quality
    img.save(jpg_filepath, format='JPEG', quality=quality)
    print(f"Converted PNG image '{png_filepath}' to JPG image '{jpg_filepath}'.")
  except FileNotFoundError:
    print(f"Error: PNG file '{png_filepath}' not found.")
  except Exception as e:
    print(f"Error converting PNG to JPG: {e}")

# Example usage
png_file = "imgs\checklist.png"
jpg_file = "imgs\checklist.jpg"

convert_png_to_jpg(png_file, jpg_file)