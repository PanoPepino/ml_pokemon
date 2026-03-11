# GPT generated

"""
Generate simple SVG badges for each Pokémon type.
- Rounded rectangles
- Vertical color gradient
- Type name text centered
"""

import os
import svgwrite

OUT_DIR = "types"
WIDTH, HEIGHT = 180, 60
RADIUS = 14
FONT_FAMILY = "DejaVu Sans, Arial, sans-serif"
FONT_SIZE = 24

# Fan-standard hex colors per type (not official assets, but close)[web:211]
TYPE_COLORS = {
    "normal":   "#B8B898",
    "fire":     "#EE8130",
    "water":    "#6390F0",
    "electric": "#F7D02C",
    "grass":    "#7AC74C",
    "ice":      "#96D9D6",
    "fighting": "#C22E28",
    "poison":   "#A33EA1",
    "ground":   "#D8AD40",
    "flying":   "#A98FF3",
    "psychic":  "#F95587",
    "bug":      "#A6B91A",
    "rock":     "#736312",
    "ghost":    "#735797",
    "dragon":   "#6F35FC",
    "dark":     "#3F2F23",
    "steel":    "#B7B7CE",
    "fairy":    "#D685AD",
}


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def lighten(hex_color, factor=0.25):
    r, g, b = hex_to_rgb(hex_color)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02X}{g:02X}{b:02X}"


def darken(hex_color, factor=0.25):
    r, g, b = hex_to_rgb(hex_color)
    r = int(r * (1 - factor))
    g = int(g * (1 - factor))
    b = int(b * (1 - factor))
    return f"#{r:02X}{g:02X}{b:02X}"


def make_badge(type_name, base_color):
    os.makedirs(OUT_DIR, exist_ok=True)
    filename = os.path.join(OUT_DIR, f"{type_name}.svg")

    dwg = svgwrite.Drawing(
        filename=filename,
        size=(WIDTH, HEIGHT),
        viewBox=f"0 0 {WIDTH} {HEIGHT}",
    )

    # Gradient id
    grad_id = f"grad_{type_name}"

    # Define vertical linear gradient
    grad = dwg.linearGradient(
        start=("0%", "0%"),
        end=("0%", "100%"),
        id=grad_id,
    )
    grad.add_stop_color(0,  lighten(base_color, 0.3))
    grad.add_stop_color(0.5, base_color)
    grad.add_stop_color(1,  darken(base_color, 0.3))
    dwg.defs.add(grad)

    # Rounded rectangle with gradient fill
    dwg.add(dwg.rect(
        insert=(0, 0),
        size=(WIDTH, HEIGHT),
        rx=RADIUS,
        ry=RADIUS,
        fill=f"url(#{grad_id})",
        stroke="#FFFFFF",
        stroke_width=2,
    ))

    # Type label (capitalized)
    label = type_name.capitalize()
    dwg.add(dwg.text(
        label,
        insert=("50%", "50%"),
        text_anchor="middle",
        dominant_baseline="middle",
        fill="#FFFFFF",
        font_size=FONT_SIZE,
        font_family=FONT_FAMILY,
        style="font-weight:bold;",
    ))

    dwg.save()
    print(f"Saved: {filename}")


def main():
    for t_name, color in TYPE_COLORS.items():
        make_badge(t_name, color)


if __name__ == "__main__":
    main()
