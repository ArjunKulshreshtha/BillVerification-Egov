import cv2
from PIL import Image
import numpy as np
# import os


# """ CAMERA PARAMETERS """
# # Cropped region of card window
# H_MIN = 75
# H_MAX = 700
# W_MIN = 550
# W_MAX = 775
# IMAGE_RESOLUTION = (1920,1080)
# IMAGE_ROTATION_DEGS = 0

BW_THRESH = 160 # 70

# Function to create a plain white image of the same dimensions as the input image
def create_white_image(input_image_path, output_image_path):
    # Read the input image
    img = cv2.imread(input_image_path)

    # Get the dimensions of the image
    height, width, channels = img.shape
    print(f"Image dimensions: {width}x{height}")

    # Create a plain white image with the same dimensions
    white_image = np.ones((height, width, channels), dtype=np.uint8) * 255

    # Create the output folder if it does not exist
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)

    # Define the output path
    # output_image_path = os.path.join(output_folder, 'white_image.png')

    # Save the white image
    cv2.imwrite(output_image_path, white_image)
    print(f"White image saved to: {output_image_path}")

def debug_save_img(img, imgname):
    im = Image.fromarray(img)
    im.save(imgname)


img_path = 'imgs/handwriting.jpg'
img_raw = cv2.imread(img_path)
# Create a white image with the same dimensions as the input image
create_white_image(img_path, 'imgs/WhiteOffset.jpg')
white_offset_img = cv2.imread('imgs\whiteOffset.jpg', cv2.IMREAD_GRAYSCALE)




gray = cv2.cvtColor(img_raw,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
morph = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

blur_crop = white_offset_img - morph
blur_crop[blur_crop > 200] = 0




debug_save_img(blur_crop, 'uploads/offset_greyscale.jpg')
debug_save_img(morph, 'uploads/greyscale.jpg')
    
# if exp_threshold is None:
exp_threshold = BW_THRESH
_, proc_img = cv2.threshold(blur_crop, exp_threshold, 255, cv2.THRESH_BINARY)

# proc_img = cv2.bitwise_not(proc_img)
# proc_img = cv2.morphologyEx(proc_img, cv2.MORPH_DILATE, kernel)
proc_img = cv2.morphologyEx(proc_img, cv2.MORPH_DILATE, kernel)
proc_img = cv2.bitwise_not(proc_img)


# if cfg.DEBUG_MODE:
debug_save_img(proc_img, 'uploads/thresholded.jpg')