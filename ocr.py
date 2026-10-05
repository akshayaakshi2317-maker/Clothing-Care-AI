import os
import re
import shutil

import cv2
import numpy as np
import pytesseract

from PIL import Image


# ============================================================
# TESSERACT CONFIGURATION
# ============================================================

tesseract_path = shutil.which("tesseract")

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

elif os.name == "nt":

    windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    if os.path.exists(windows_path):
        pytesseract.pytesseract.tesseract_cmd = windows_path


# ============================================================
# FABRIC LIST
# ============================================================

FABRICS = [
    "COTTON",
    "POLYESTER",
    "VISCOSE",
    "RAYON",
    "SILK",
    "WOOL",
    "NYLON",
    "LINEN",
    "ELASTANE",
    "ACRYLIC",
    "DENIM",
    "SPANDEX"
]


# ============================================================
# OCR ERROR CORRECTION
# ============================================================

OCR_CORRECTIONS = {

    "C0TTON": "COTTON",
    "COTT0N": "COTTON",

    "P0LYESTER": "POLYESTER",
    "POLYEST3R": "POLYESTER",

    "VISC0SE": "VISCOSE",

    "RAY0N": "RAYON",

    "NYL0N": "NYLON",

    "ACRYL1C": "ACRYLIC",

    "ELAST4NE": "ELASTANE",

    "L1NEN": "LINEN",

    "S1LK": "SILK",

    "W0OL": "WOOL",

    "D3NIM": "DENIM",

    "SP4NDEX": "SPANDEX",

    "DONOT": "DO NOT",

    "D0 NOT": "DO NOT",

    "MEOIUM": "MEDIUM",
    "MEDlUM": "MEDIUM",
    "MEDIOM": "MEDIUM",
    "MED1UM": "MEDIUM",

    "L0W": "LOW",
    "H1GH": "HIGH",

    "C0LD": "COLD",

    "TUMBLEDRY": "TUMBLE DRY",

    "DRYCLEAN": "DRY CLEAN",

    "WASHCOLD": "WASH COLD",

    "HANDWASH": "HAND WASH",

    "LINE DRY": "LINE DRY",

    "DRYFLAT": "DRY FLAT",

    "DONOTWRING": "DO NOT WRING",

    "WASHINSIDEOUT": "WASH INSIDE OUT",

    "IRONONREVERSE": "IRON ON REVERSE"
}


# ============================================================
# CARE PHRASES
# ============================================================

CARE_PHRASES = [
    "MACHINE WASH",
    "HAND WASH",
    "WASH AT",
    "WASH COLD",
    "WASH WITH SIMILAR COLOURS",
    "WASH WITH SIMILAR COLORS",
    "WASH INSIDE OUT",

    "DO NOT BLEACH",
    "NO BLEACH",

    "TUMBLE DRY",
    "DO NOT TUMBLE DRY",
    "DRY FLAT",
    "LINE DRY",

    "IRON LOW",
    "IRON MEDIUM",
    "IRON HIGH",
    "DO NOT IRON",
    "IRON ON REVERSE",

    "DRY CLEAN",
    "DO NOT DRY CLEAN",

    "DO NOT WRING",
    "WRING"
]


# ============================================================
# IMAGE PREPROCESSING
# ============================================================

def preprocess_image(image):

    img = np.array(image)

    if len(img.shape) == 3:

        img = cv2.cvtColor(
            img,
            cv2.COLOR_RGB2BGR
        )

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    # Upscale
    gray = cv2.resize(
        gray,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    # Noise removal
    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    # Contrast enhancement
    clahe = cv2.createCLAHE(
        clipLimit=2.5,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    return enhanced


# ============================================================
# CREATE OCR VARIANTS
# ============================================================

def create_variants(gray):

    variants = []

    # Original
    variants.append(gray)

    # OTSU
    _, otsu = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    variants.append(otsu)

    # Adaptive threshold
    adaptive = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    variants.append(adaptive)

    # Inverted OTSU
    _, inverted = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    variants.append(inverted)

    return variants


# ============================================================
# CORRECT OCR TEXT
# ============================================================

def correct_ocr(text):

    text = text.upper()

    for wrong, correct in OCR_CORRECTIONS.items():

        text = text.replace(
            wrong,
            correct
        )

    # Normalize spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # Restore common phrases
    replacements = {

        "MACHINE WASH COLD":
            "MACHINE WASH COLD",

        "WASH AT 40 C":
            "WASH AT 40°C",

        "WASH AT 30 C":
            "WASH AT 30°C",

        "WASH AT 40°C":
            "WASH AT 40°C",

        "WASH AT 30°C":
            "WASH AT 30°C",

        "TUMBLE DRY LOW":
            "TUMBLE DRY LOW",

        "TUMBLE DRY MEDIUM":
            "TUMBLE DRY MEDIUM",

        "TUMBLE DRY HIGH":
            "TUMBLE DRY HIGH",

        "IRON LOW":
            "IRON LOW",

        "IRON MEDIUM":
            "IRON MEDIUM",

        "IRON HIGH":
            "IRON HIGH"
    }

    for wrong, correct in replacements.items():

        text = text.replace(
            wrong,
            correct
        )

    return text


# ============================================================
# USEFUL OCR LINE
# ============================================================

def useful_line(line):

    line = line.strip().upper()

    if not line:
        return False

    # Percentage
    if re.search(r"\d+\s*%", line):
        return True

    # Temperature
    if re.search(r"\d+\s*°?\s*C", line):
        return True

    # Fabric
    for fabric in FABRICS:

        if fabric in line:
            return True

    # Care words
    words = [
        "WASH",
        "BLEACH",
        "TUMBLE",
        "DRY",
        "IRON",
        "CLEAN",
        "WRING",
        "COLOUR",
        "COLOR",
        "REVERSE"
    ]

    for word in words:

        if word in line:
            return True

    return False


# ============================================================
# CLEAN OCR
# ============================================================

def clean_text(text):

    text = correct_ocr(text)

    lines = []

    for raw_line in text.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        # Remove noisy characters
        line = re.sub(
            r"^[^A-Z0-9]+",
            "",
            line.upper()
        )

        line = re.sub(
            r"\s+",
            " ",
            line
        )

        # Fix percentage spacing
        line = re.sub(
            r"(\d+)\s+%",
            r"\1%",
            line
        )

        # Fix temperature
        line = re.sub(
            r"(\d+)\s*°?\s*C",
            r"\1°C",
            line
        )

        if useful_line(line):

            if line not in lines:
                lines.append(line)

    return "\n".join(lines)


# ============================================================
# OCR EXTRACTION
# ============================================================

def extract_text(image):

    gray = preprocess_image(image)

    variants = create_variants(gray)

    configs = [
        "--psm 6",
        "--psm 11",
        "--psm 12"
    ]

    results = []

    for variant in variants:

        for config in configs:

            try:

                text = pytesseract.image_to_string(
                    variant,
                    config=config
                )

                if text.strip():

                    results.append(text)

            except Exception:
                pass

    combined = "\n".join(results)

    cleaned = clean_text(
        combined
    )

    return cleaned.strip()
