import math
import numpy as np
import sys
from colour.models import sRGB_to_XYZ, XYZ_to_Oklab

if "--snark" in sys.argv:
    from .snark import COLOUR_NAMES
else:
    from .colours import COLOUR_NAMES

def rgb_to_lab(r, g, b):
    """Convert RGB colours to LAB colours."""
    inputColor = [r, g, b]
    num = 0
    RGB = [0, 0, 0]
    for value in inputColor:
        value = float(value) / 255
        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value = value / 12.92
        RGB[num] = value * 100
        num = num + 1
    XYZ = [0, 0, 0]
    X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
    Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
    Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
    XYZ[0] = round(X, 4)
    XYZ[1] = round(Y, 4)
    XYZ[2] = round(Z, 4)

    XYZ[0] = float(XYZ[0]) / 95.047   # ref_X =  95.047
    XYZ[1] = float(XYZ[1]) / 100.0    # ref_Y = 100.000
    XYZ[2] = float(XYZ[2]) / 108.883  # ref_Z = 108.883

    num = 0
    for value in XYZ:
        if value > 0.008856:
            value = value ** (0.3333333333333333)
        else:
            value = (7.787 * value) + (16 / 116)
        XYZ[num] = value
        num = num + 1

    Lab = [0, 0, 0]
    L = (116 * XYZ[1]) - 16
    a = 500 * (XYZ[0] - XYZ[1])
    b = 200 * (XYZ[1] - XYZ[2])

    Lab[0] = round(L, 4)
    Lab[1] = round(a, 4)
    Lab[2] = round(b, 4)

    return Lab

def rgb_to_oklch(r, g, b):
    """Convert RGB (0-255) to OKLCH color space, output L and C in [0,1], H in degrees."""
    rgb_normalized = np.array([r / 255.0, g / 255.0, b / 255.0])
    xyz = sRGB_to_XYZ(rgb_normalized)
    oklab = XYZ_to_Oklab(xyz)
    L, a, b_val = oklab
    C = np.sqrt(a**2 + b_val**2)
    H = np.degrees(np.arctan2(b_val, a)) % 360
    return (L, C, H)

def deltaE(labA, labB):
    """deltaE is the standard way to compare two colours for how visibly alike they are"""
    deltaL = labA[0] - labB[0]
    deltaA = labA[1] - labB[1]
    deltaB = labA[2] - labB[2]
    c1 = math.sqrt(labA[1] * labA[1] + labA[2] * labA[2])
    c2 = math.sqrt(labB[1] * labB[1] + labB[2] * labB[2])
    deltaC = c1 - c2
    deltaH = deltaA * deltaA + deltaB * deltaB - deltaC * deltaC
    if deltaH < 0:
        deltaH = 0
    else:
        deltaH = math.sqrt(deltaH)
    sc = 1.0 + 0.045 * c1
    sh = 1.0 + 0.015 * c1
    deltaLKlsl = deltaL / (1.0)
    deltaCkcsc = deltaC / (sc)
    deltaHkhsh = deltaH / (sh)
    i = (deltaLKlsl * deltaLKlsl + deltaCkcsc * deltaCkcsc + deltaHkhsh * deltaHkhsh)
    if i < 0:
        return 0
    else:
        return math.sqrt(i)

LAB_COLOUR_NAMES = [(rgb_to_lab(x[0], x[1], x[2]), x[3]) for x in COLOUR_NAMES]
