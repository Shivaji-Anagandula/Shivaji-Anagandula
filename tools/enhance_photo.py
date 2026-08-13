# tools/enhance_photo.py
import cv2
import numpy as np
import os


def enhance_for_ascii(input_path="Shivaji Anagandula.png", output_path="assets/enhanced_grayscale.png"):
    # Ensure assets directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Read the original photo
    img = cv2.imread(input_path)
    if img is None:
        raise FileNotFoundError(
            f"Original photo not found at '{input_path}'. Please check the file path.")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Contrast Limited Adaptive Histogram Equalization (CLAHE) for likeness detail
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Invert tones so dark regions map correctly to dense ASCII characters
    inverted_final = cv2.bitwise_not(enhanced)

    # Resize to width=120 while maintaining corrected aspect ratio
    target_width = 120
    h, w = gray.shape
    aspect_ratio = h / w
    # ASCII character height correction
    target_height = int(target_width * aspect_ratio * 0.55)
    resized = cv2.resize(inverted_final, (target_width,
                         target_height), interpolation=cv2.INTER_AREA)

    # Save processed image
    cv2.imwrite(output_path, resized)
    print(f"Enhanced grayscale photo successfully saved to '{output_path}'.")


if __name__ == "__main__":
    enhance_for_ascii()
