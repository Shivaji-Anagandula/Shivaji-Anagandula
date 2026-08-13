# tools/render_clean_hd_portrait.py
import cv2
import numpy as np
import os


def render_hd_clean_ascii(input_path="Shivaji Anagandula.png", output_path="portrait.svg?v=2"):
    # Read the photo
    img = cv2.imread(input_path)
    if img is None:
        raise FileNotFoundError(f"Could not find '{input_path}'.")

    # 1. High resolution width for clear face detail (80 characters wide)
    target_width = 80
    h, w, _ = img.shape
    aspect_ratio = h / w
    target_height = int(target_width * aspect_ratio * 0.5)

    resized = cv2.resize(img, (target_width, target_height),
                         interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # 2. Enhance facial features with CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # 3. Create a clean mask to remove background noise (focus strictly on subject)
    # Uses adaptive thresholding to retain facial contours without background clutter
    mask = cv2.adaptiveThreshold(
        enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # 4. Detailed ASCII character ramp from dark to light
    ASCII_RAMP = " $@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    cell_size = 8
    svg_width = target_width * cell_size
    svg_height = target_height * cell_size

    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}" font-family="monospace">\n')
    svg.append('  <style>\n')
    # Vibrant Cyan
    svg.append(
        '    text { font-size: 9px; fill: #00F0FF; font-weight: bold; }\n')
    svg.append('  </style>\n')

    # Build static SVG
    for y in range(target_height):
        for x in range(target_width):
            # Skip background pixels to keep output clean & lightweight
            if mask[y, x] > 200 and enhanced[y, x] > 180:
                continue

            pixel_val = enhanced[y, x]
            char_idx = int((pixel_val / 255.0) * (len(ASCII_RAMP) - 1))
            char = ASCII_RAMP[char_idx]

            # Escape special XML chars
            if char == '<':
                char = '&lt;'
            elif char == '>':
                char = '&gt;'
            elif char == '&':
                char = '&amp;'

            sx = x * cell_size
            sy = y * cell_size + cell_size
            svg.append(f'  <text x="{sx}" y="{sy}">{char}</text>\n')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(svg)

    print(f"Clean HD portrait successfully generated at '{output_path}'!")


if __name__ == "__main__":
    render_hd_clean_ascii()
