# tools/render_panel.py
import os
import html
import textwrap

ROWS = [
    ("role", "Developer | Technical Consultant"),
    ("focus", "Azure AI Engineer & Microsoft Dynamics 365 F&O"),
    ("stack", "Microsoft Copilot Studio · Power Automate · RAG · LangChain · Azure OpenAI Service · Azure AI Foundry · Azure Cognitive Services · Python"),
    ("now", "Integrating Azure AI Document Intelligence with D365 along with RAG pipelines, Azure AI Search, and Azure OpenAI to generate natural-language answers."),
]

HEADER_TITLE = "shivaji@terminal:~$"
ACCENT_COLOR = "#00F0FF"


def render_panel_svg(output_path="sysinfo.svg"):
    is_preview = os.environ.get("PREVIEW") == "1"

    width = 750
    padding = 24
    header_height = 38
    line_height = 20
    section_gap = 16  # Extra breathing room between fields

    processed_rows = []
    current_y = header_height + padding + 12

    for label, val in ROWS:
        # Wrap long text cleanly
        wrapped_lines = textwrap.wrap(val, width=68)

        escaped_label = html.escape(label)
        escaped_lines = [html.escape(line) for line in wrapped_lines]

        processed_rows.append({
            "label": escaped_label,
            "lines": escaped_lines,
            "y": current_y
        })

        # Calculate Y for the next field based on lines in this field + gap
        current_y += (len(escaped_lines) * line_height) + section_gap

    height = current_y + padding - section_gap + 10

    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">\n')
    svg.append('<style>\n')
    svg.append(
        '  .bg { fill: #0d1117; rx: 8px; ry: 8px; stroke: #30363d; stroke-width: 1px; }\n')
    svg.append(
        '  .header { font-family: monospace; font-size: 12px; fill: #8b949e; font-weight: bold; }\n')
    svg.append(
        '  .label { font-family: monospace; font-size: 13px; fill: #7ee787; font-weight: bold; }\n')
    svg.append(
        '  .val { font-family: monospace; font-size: 13px; fill: #c9d1d9; }\n')
    svg.append(f'  .accent {{ fill: {ACCENT_COLOR}; }}\n')

    if not is_preview:
        svg.append(
            '  @keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }\n')
        svg.append(
            '  .row-anim { animation: fadeIn 0.4s ease-out forwards; opacity: 0; }\n')

    svg.append('</style>\n')

    # Terminal Container
    svg.append(f'<rect width="{width}" height="{height}" class="bg" />\n')

    # Terminal Header
    svg.append('<circle cx="20" cy="20" r="5" fill="#ff5f56" />\n')
    svg.append('<circle cx="36" cy="20" r="5" fill="#ffbd2e" />\n')
    svg.append('<circle cx="52" cy="20" r="5" fill="#27c93f" />\n')
    svg.append(
        f'<text x="72" y="24" class="header">{html.escape(HEADER_TITLE)}</text>\n')
    svg.append(
        f'<line x1="0" y1="{header_height}" x2="{width}" y2="{header_height}" stroke="#30363d" stroke-width="1" />\n')

    # Content Rows
    for i, row in enumerate(processed_rows):
        delay = 0.2 + (i * 0.15)
        anim_class = f'class="row-anim" style="animation-delay: {delay:.2f}s;"' if not is_preview else ''

        row_svg = f'<g {anim_class}>\n'
        row_svg += f'  <text x="24" y="{row["y"]}" class="label">{row["label"]}:</text>\n'

        for line_idx, line in enumerate(row["lines"]):
            line_y = row["y"] + (line_idx * line_height)
            row_svg += f'  <text x="95" y="{line_y}" class="val">{line}</text>\n'

        row_svg += '</g>\n'
        svg.append(row_svg)

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(svg)
    print(f"Info panel updated at {output_path}")


if __name__ == "__main__":
    render_panel_svg("sysinfo.svg")
