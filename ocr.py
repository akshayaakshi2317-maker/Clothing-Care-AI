import os
import re
import shutil

import cv2
import numpy as np
import pytesseract


# ============================================================
# TESSERACT SETUP
# Works on Windows + Streamlit Cloud
# ============================================================

def setup_tesseract():

    # Streamlit Cloud / Linux
    tesseract_path = shutil.which("tesseract")

    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        return

    # Windows
    windows_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    ]

    for path in windows_paths:

        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            return


setup_tesseract()


# ============================================================
# VALID FABRICS
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
# VALID COUNTRIES
# ============================================================

COUNTRIES = [
    "INDIA",
    "CHINA",
    "ITALY",
    "UK",
    "VIETNAM",
    "TURKEY",
    "INDONESIA",
    "BANGLADESH",
    "PAKISTAN"
]


# ============================================================
# OCR COMMON MISTAKE CORRECTIONS
# ============================================================

def correct_common_errors(text):

    replacements = {

        "C0TTON": "COTTON",
        "COTT0N": "COTTON",

        "P0LYESTER": "POLYESTER",
        "POLYEST3R": "POLYESTER",

        "VISC0SE": "VISCOSE",

        "RAY0N": "RAYON",

        "NYL0N": "NYLON",

        "S1LK": "SILK",

        "W0OL": "WOOL",

        "L1NEN": "LINEN",

        "ELAST4NE": "ELASTANE",

        "ACRYL1C": "ACRYLIC",

        "D3NIM": "DENIM",

        "SP4NDEX": "SPANDEX",

        "DONOT": "DO NOT",

        "MACHINEWASH": "MACHINE WASH",

        "HANDWASH": "HAND WASH",

        "WASHCOLD": "WASH COLD",

        "TUMBLEDRY": "TUMBLE DRY",

        "DRYCLEAN": "DRY CLEAN",

        "DRYFLAT": "DRY FLAT",

        "LINEDRY": "LINE DRY",

        "MEOIUM": "MEDIUM",

        "MEDlUM": "MEDIUM",

        "MED1UM": "MEDIUM",

        "MEDIOM": "MEDIUM",

        "IND0NESIA": "INDONESIA",

        "CH1NA": "CHINA",

        "VIETN4M": "VIETNAM"
    }

    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    return text


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):

    text = text.upper()

    # Remove unwanted OCR symbols
    text = text.replace("®", " ")
    text = text.replace("©", " ")
    text = text.replace("™", " ")

    # Replace punctuation with spaces
    text = text.replace("|", " ")
    text = text.replace(":", " ")
    text = text.replace(";", " ")

    # Common OCR corrections
    text = correct_common_errors(text)

    # Remove repeated spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


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

    # Improve contrast
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    gray = clahe.apply(gray)

    # Reduce small noise
    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    return gray


# ============================================================
# THRESHOLD IMAGE
# ============================================================

def threshold_image(gray):

    binary = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    return binary


# ============================================================
# RUN ONE OCR
# IMPORTANT:
# DO NOT MERGE MULTIPLE OCR RESULTS
# ============================================================

def run_single_ocr(image):

    try:

        text = pytesseract.image_to_string(
            image,
            config="--psm 6"
        )

        return text

    except Exception:

        return ""


# ============================================================
# VALID FABRIC EXTRACTION
# ============================================================

def extract_fabric(text):

    results = []

    pattern = r"(\d{1,3})\s*%\s*([A-Z]+)"

    matches = re.findall(
        pattern,
        text
    )

    for percentage, fabric in matches:

        fabric = fabric.upper()

        if fabric in FABRICS:

            line = f"{percentage}% {fabric}"

            if line not in results:
                results.append(line)

    # Denim (Cotton)
    if "DENIM" in text:

        if "COTTON" in text:

            if not any(
                "DENIM" in x
                for x in results
            ):

                results.append(
                    "DENIM (COTTON)"
                )

        elif not any(
            "DENIM" in x
            for x in results
        ):

            results.append(
                "DENIM"
            )

    return results


# ============================================================
# WASHING
# ============================================================

def extract_washing(text):

    if "HAND WASH COLD" in text:
        return "HAND WASH COLD"

    if "HAND WASH" in text:
        return "HAND WASH"

    match = re.search(
        r"WASH\s*AT\s*(\d+)\s*°?\s*C",
        text
    )

    if match:

        return (
            "WASH AT "
            + match.group(1)
            + "°C"
        )

    if "MACHINE WASH COLD" in text:
        return "MACHINE WASH COLD"

    if "MACHINE WASH" in text:
        return "MACHINE WASH"

    if "WASH COLD" in text:
        return "WASH COLD"

    if "WASH WITH SIMILAR COLOURS" in text:
        return "WASH WITH SIMILAR COLOURS"

    if "WASH WITH SIMILAR COLORS" in text:
        return "WASH WITH SIMILAR COLORS"

    return None


# ============================================================
# BLEACHING
# ============================================================

def extract_bleaching(text):

    if "DO NOT BLEACH" in text:
        return "DO NOT BLEACH"

    if "NO BLEACH" in text:
        return "NO BLEACH"

    return None


# ============================================================
# DRYING
# ============================================================

def extract_drying(text):

    if "DO NOT TUMBLE DRY" in text:
        return "DO NOT TUMBLE DRY"

    if "TUMBLE DRY LOW" in text:
        return "TUMBLE DRY LOW"

    if "TUMBLE DRY MEDIUM" in text:
        return "TUMBLE DRY MEDIUM"

    if "TUMBLE DRY HIGH" in text:
        return "TUMBLE DRY HIGH"

    if "DRY FLAT" in text:
        return "DRY FLAT"

    if "LINE DRY" in text:
        return "LINE DRY"

    if "TUMBLE DRY" in text:
        return "TUMBLE DRY"

    return None


# ============================================================
# IRONING
# ============================================================

def extract_ironing(text):

    if "DO NOT IRON" in text:
        return "DO NOT IRON"

    if "IRON LOW" in text:
        return "IRON LOW"

    if "IRON MEDIUM" in text:
        return "IRON MEDIUM"

    if "IRON HIGH" in text:
        return "IRON HIGH"

    if "IRON ON REVERSE" in text:
        return "IRON ON REVERSE"

    return None


# ============================================================
# DRY CLEANING
# ============================================================

def extract_cleaning(text):

    if "DO NOT DRY CLEAN" in text:
        return "DO NOT DRY CLEAN"

    if "DRY CLEAN" in text:
        return "DRY CLEAN"

    return None


# ============================================================
# SPECIAL INSTRUCTIONS
# ============================================================

def extract_special(text):

    results = []

    if "WASH INSIDE OUT" in text:
        results.append(
            "WASH INSIDE OUT"
        )

    if "DO NOT WRING" in text:
        results.append(
            "DO NOT WRING"
        )

    if "IRON ON REVERSE" in text:
        results.append(
            "IRON ON REVERSE"
        )

    if "WASH WITH SIMILAR COLOURS" in text:
        results.append(
            "WASH WITH SIMILAR COLOURS"
        )

    if "WASH WITH SIMILAR COLORS" in text:
        results.append(
            "WASH WITH SIMILAR COLORS"
        )

    return results


# ============================================================
# COUNTRY
# ============================================================

def extract_country(text):

    match = re.search(
        r"MADE\s+IN\s+([A-Z]+)",
        text
    )

    if match:

        country = match.group(1)

        if country in COUNTRIES:

            return (
                "MADE IN "
                + country
            )

    return None


# ============================================================
# BUILD CLEAN FINAL OCR
# ============================================================

def build_clean_result(text):

    text = normalize_text(text)

    final_lines = []

    # -------------------------
    # Fabric
    # -------------------------

    fabrics = extract_fabric(text)

    for item in fabrics:

        if item not in final_lines:

            final_lines.append(item)

    # -------------------------
    # Washing
    # -------------------------

    washing = extract_washing(text)

    if washing:

        final_lines.append(washing)

    # -------------------------
    # Bleaching
    # -------------------------

    bleaching = extract_bleaching(text)

    if bleaching:

        final_lines.append(bleaching)

    # -------------------------
    # Drying
    # -------------------------

    drying = extract_drying(text)

    if drying:

        final_lines.append(drying)

    # -------------------------
    # Ironing
    # -------------------------

    ironing = extract_ironing(text)

    if ironing:

        final_lines.append(ironing)

    # -------------------------
    # Dry Cleaning
    # -------------------------

    cleaning = extract_cleaning(text)

    if cleaning:

        final_lines.append(cleaning)

    # -------------------------
    # Special Instructions
    # -------------------------

    special = extract_special(text)

    for item in special:

        if item not in final_lines:

            final_lines.append(item)

    # -------------------------
    # Country
    # -------------------------

    country = extract_country(text)

    if country:

        final_lines.append(country)

    # -------------------------
    # Remove duplicates
    # -------------------------

    unique_lines = []

    for line in final_lines:

        if line not in unique_lines:

            unique_lines.append(line)

    return "\n".join(
        unique_lines
    )


# ============================================================
# MAIN FUNCTION USED BY APP.PY
# ============================================================

def extract_text(image):

    # Preprocess image
    gray = preprocess_image(
        image
    )

    # Create threshold version
    binary = threshold_image(
        gray
    )

    # --------------------------------------------------------
    # Run OCR on BOTH versions
    # But DO NOT concatenate their outputs.
    # Select the better result.
    # --------------------------------------------------------

    text_original = run_single_ocr(
        gray
    )

    text_binary = run_single_ocr(
        binary
    )

    # Choose result with more useful clothing keywords
    keywords = [
        "COTTON",
        "POLYESTER",
        "RAYON",
        "VISCOSE",
        "SILK",
        "WOOL",
        "NYLON",
        "LINEN",
        "DENIM",
        "MACHINE",
        "HAND",
        "WASH",
        "BLEACH",
        "TUMBLE",
        "DRY",
        "IRON",
        "MADE"
    ]

    score_original = sum(
        word in text_original.upper()
        for word in keywords
    )

    score_binary = sum(
        word in text_binary.upper()
        for word in keywords
    )

    if score_binary > score_original:

        selected_text = text_binary

    else:

        selected_text = text_original

    # Build structured clean result
    final_text = build_clean_result(
        selected_text
    )

    return final_text
