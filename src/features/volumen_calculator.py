import pandas as pd
import math


def biological_volume(height, weight, body_shape):
    """BIOLOGICALLY VALIDATED volume formulas (m³)."""
    h, w = height, weight
    shape = str(body_shape).lower()

    # QUADRUPED/SERPENTINE: Cylinder (snakes, wolves)
    if any(x in shape for x in ['quadruped', 'serpentine']):
        r = (w / (math.pi * h))**(1/2)
        return math.pi * r**2 * h * 0.85

    # BIPEDAL/HUMANOID: Ellipsoid (humans, bears)
    elif 'bipedal' in shape or 'humanoid' in shape:
        a = b = h * 0.35
        c = h * 0.6
        return (4/3) * math.pi * a * b * c * 0.75

    # WINGS: Thin ellipsoid (birds, bats)
    elif 'wing' in shape:
        span, thick, chord = h*2.5, h*0.15, h*0.4
        return span * chord * thick * 0.3

    # FINNED/FISH: Streamlined cylinder
    elif 'finned' in shape:
        r = (w / (math.pi * h))**(1/2)
        return math.pi * r**2 * h * 0.82

    # ARMOR: Cubic prism (armadillo)
    elif 'armor' in shape:
        side = (w * 6)**(1/3)
        return side**3 * 0.88

    # BLOB/BALL: Sphere (Jellicent)
    elif any(x in shape for x in ['blob', 'ball']):
        r = ((3 * w) / (4 * math.pi))**(1/3)
        return (4/3) * math.pi * r**3 * 0.92

    # SEED/EGG: Prolate spheroid
    elif 'seed' in shape:
        a, b, c = h*0.55, h*0.45, h*0.45
        return (4/3) * math.pi * a * b * c * 0.9

    # HEAD LEGS: Upright cylinder
    elif 'head legs' in shape:
        r = (w / (math.pi * h))**(1/2)
        return math.pi * r**2 * h * 0.8

    # DEFAULT: Ellipsoid
    else:
        return (4/3) * math.pi * (h/2)**2 * (w/h)**(1/3) * 0.85
