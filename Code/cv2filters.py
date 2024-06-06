import cv2

def convert_to_grayscale(image_path):
    """Convert the image to grayscale and save it with a '_gray' postfix."""
    img = cv2.imread(image_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    output_path = image_path.replace('.', '_gray.')
    cv2.imwrite(output_path, gray_img)
    print(f"Grayscale image saved to: {output_path}")
    return output_path



def apply_threshold(image_path, threshold_value):
    """Apply binary threshold to the grayscale image."""
    gray_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_img = cv2.threshold(gray_img, threshold_value, 255, cv2.THRESH_BINARY)
    output_path = image_path.replace('_gray.', f'_binary_{threshold_value}.')
    cv2.imwrite(output_path, binary_img)
    print(f"Binary image saved to: {output_path}")
    return output_path


def process_image(image_path, kernel_size=(3, 3), blur_ksize=(5, 5), exp_threshold=160):
    print('method called')
    """Perform morphological processing and other image operations."""
    gray_img_path = convert_to_grayscale(image_path)
    binary_img_path = apply_threshold(gray_img_path, exp_threshold)
    
    img = cv2.imread(binary_img_path, cv2.IMREAD_GRAYSCALE)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    morph_img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    

    output_path = image_path.replace('.jpg', '_processed.jpg')
    cv2.imwrite(output_path, morph_img)
    print(f"Processed image saved to: {output_path}")
    return output_path