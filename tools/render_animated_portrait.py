# tools/render_animated_portrait.py
import cv2
import numpy as np
import os
import random


def create_animated_ascii_svg(image_path="assets/enhanced_grayscale.png", output_path="portrait.svg"):
    # Multi-tone ASCII ramp for capturing face detail and facial likeness
    ASCII_CHARS = "@%#*+=-:. "

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(
            f"Image not found at '{image_path}'. Run 'python tools/enhance_photo.py' first.")

    h, w = img.shape

    cell_size = 6
    width = w * cell_size
    height = h * cell_size

    p_grid_cell_size = cell_size * 2
    particles_x = width // p_grid_cell_size
    particles_y = height // p_grid_cell_size

    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" font-family="monospace">\n')
    svg.append('<style>\n')
    svg.append('  text { font-size: 8px; fill: #00F0FF; }\n')  # Primary Cyan
    svg.append('  .p-char { font-size: 5px; fill: #0088AA; opacity: 0.2; }\n')
    svg.append('  @keyframes floatChar {\n')
    svg.append(
        '    0% { transform: translate(0px, 0px) scale(0); opacity: 0; }\n')
    svg.append(
        '    2% { transform: translate(0px, 0px) scale(1); opacity: 0.5; }\n')
    svg.append(
        '    10% { transform: translate(0px, 0px) scale(1.1); opacity: 0.7; }\n')
    svg.append(
        '    20% { transform: translate(var(--x, 0px), var(--y, 0px)) scale(1.0); opacity: 1; }\n')
    svg.append(
        '    80% { transform: translate(var(--x, 0px), var(--y, 0px)) scale(1.0); opacity: 1; }\n')
    svg.append(
        '    98% { transform: translate(calc(var(--x, 0px)*1.2), calc(var(--y, 0px)*0.8)) scale(1.1); opacity: 0.5; }\n')
    svg.append(
        '    100% { transform: translate(calc(var(--x, 0px)*1.5), calc(var(--y, 0px)*0.5)) scale(0.1); opacity: 0; }\n')
    svg.append('  }\n')
    svg.append('</style>\n')

    # Base multi-tone static portrait
    for y in range(h):
        for x in range(w):
            pixel_val = img[y, x]
            char_index = int((pixel_val / 255.0) * (len(ASCII_CHARS) - 1))
            ascii_char = ASCII_CHARS[char_index]

            sx = x * cell_size
            sy = y * cell_size + cell_size

            svg.append(f'  <text x="{sx}" y="{sy}">{ascii_char}</text>\n')

    # Animated particle overlay layer
    for py in range(particles_y):
        for px in range(particles_x):
            detailed_y = py * 2
            detailed_x = px * 2
            if detailed_y >= h or detailed_x >= w:
                continue

            pixel_val = img[detailed_y, detailed_x]
            char_index = int((pixel_val / 255.0) * (len(ASCII_CHARS) - 1))
            ascii_char = ASCII_CHARS[char_index]

            dest_x = px * p_grid_cell_size + cell_size
            dest_y = py * p_grid_cell_size + cell_size

            duration = 18.0
            anim_delay = random.uniform(0.1, 4.0)
            float_x = random.uniform(-150, 150)
            float_y = random.uniform(-50, 150)

            svg.append(
                f'  <g transform="translate({dest_x} {dest_y})" style="--x: {float_x}px; --y: {float_y}px; animation: floatChar {duration}s ease-in-out {anim_delay}s infinite alternate;">\n')
            svg.append(
                f'    <text class="p-char" x="0" y="0">{ascii_char}</text>\n')

            for _ in range(2):
                nx = random.uniform(-5, 5)
                ny = random.uniform(-5, 5)
                noise_char = random.choice(ASCII_CHARS[:-2])
                svg.append(
                    f'    <text class="p-char" x="{nx}" y="{ny}" fill="#0088AA" opacity="0.1">{noise_char}</text>\n')

            svg.append('  </g>\n')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(svg)
    print(
        f"Animated multi-tone portrait successfully generated at '{output_path}'.")


if __name__ == "__main__":
    create_animated_ascii_svg()
