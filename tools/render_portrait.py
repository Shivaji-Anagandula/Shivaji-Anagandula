import numpy as np
from PIL import Image

# Soft contrast character ramp (light to dark)
GLYPHS = " '`^\",:;Il!i>~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
ACCENT_COLOR = "#00F0FF"  # Cyan terminal glow


def render_ascii_svg(input_path, output_path, cols=60):
    img = Image.open(input_path).convert('L')

    # Resize keeping aspect ratio
    w, h = img.size
    aspect_ratio = h / w
    rows = int(cols * aspect_ratio * 0.5)
    img = img.resize((cols, rows))

    pixels = np.array(img)

    # Construct SVG lines
    svg_lines = []
    svg_header = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cols * 7} {rows * 10}" width="100%" height="100%">\n'
    svg_header += '<style>\n'
    svg_header += f'  .ascii {{ font-family: monospace; font-size: 8px; fill: {ACCENT_COLOR}; white-space: pre; }}\n'
    svg_header += '  @keyframes drawRow {{ to {{ width: 100%; }} }}\n'
    svg_header += '</style>\n'
    svg_header += '<rect width="100%" height="100%" fill="#0d1117" />\n'

    svg_lines.append(svg_header)

    num_glyphs = len(GLYPHS) - 1
    for r in range(rows):
        row_str = ""
        for c in range(cols):
            val = pixels[r, c]
            char_idx = int((255 - val) / 255 * num_glyphs)
            char = GLYPHS[char_idx]
            if char == '<':
                char = '&lt;'
            elif char == '>':
                char = '&gt;'
            elif char == '&':
                char = '&amp;'
            row_str += char

        delay = r * 0.04
        group = f'<g style="clip-path: inset(0 0 0 0); animation: drawRow 0.5s ease-out {delay}s forwards;">'
        text_node = f'  <text x="5" y="{(r + 1) * 9}" class="ascii">{row_str}</text>'
        svg_lines.append(f'{group}\n  {text_node}\n</g>\n')

    svg_lines.append('</svg>')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(svg_lines)
    print(f"Animated portrait written to {output_path}")


if __name__ == "__main__":
    render_ascii_svg("assets/photo-ready.png", "portrait.svg")
