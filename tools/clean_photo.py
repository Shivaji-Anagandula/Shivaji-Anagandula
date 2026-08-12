import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove


def process_photo(input_path, output_path):
    # 1. Remove background using rembg
    inp = Image.open(input_path)
    output = remove(inp)

    # Convert RGBA to OpenCV format
    img_rgba = np.array(output)

    # 2. Extract alpha mask and RGB
    rgb = img_rgba[:, :, :3]
    alpha = img_rgba[:, :, 3]

    # Convert RGB to grayscale
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    # 3. Enhance contrast using OpenCV CLAHE
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # 4. Place onto a pure white canvas
    white_bg = np.ones_like(enhanced) * 255
    final_img = np.where(alpha > 10, enhanced, white_bg)

    # Save prepared PNG
    Image.fromarray(final_img.astype('uint8')).save(output_path)
    print(f"Photo cleaned and saved to {output_path}")


if __name__ == "__main__":
    photo_name = sys.argv[1] if len(sys.argv) > 1 else "Shivaji Anagandula.png"
    process_photo(photo_name, "assets/photo-ready.png")
