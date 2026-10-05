import os
import re
import shutil

import cv2
import numpy as np
import pytesseract


# ============================================================
# TESSERACT CONFIGURATION
# ============================================================

def setup_tesseract():

    # Streamlit Cloud / Linux
    path = shutil.which("tesseract")

    if path:
        pytesseract.pytesseract.tesseract_cmd = path
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
# OCR WORD CORRECTIONS
# ============================================================

CORRECTIONS = {

    # Fabrics
    "C0TTON": "COTTON",
    "COTT0N": "COTTON",
    "COTTOON": "COTTON",

    "P0LYESTER": "POLYESTER",
    "POLYEST3R": "POLYESTER",

    "VISC0SE": "VISCOSE",
    "VISC0S3": "VISCOSE",

    "RAY0N": "RAYON",

    "NYL0N": "NYLON",

    "S1LK": "SILK",

    "W0OL": "WOOL",

    "L1NEN": "LINEN",

    "ELAST4NE": "ELASTANE",

    "ACRYL1C": "ACRYLIC",

    "D3NIM": "DENIM",

    "SP4NDEX": "SPANDEX",

    # Care words
    "DONOT": "DO NOT",
    "D0NOT": "DO NOT",

    "MACHINEWASH": "MACHINE WASH",
    "HANDWASH": "HAND WASH",

    "WASHCOLD": "WASH COLD",
    "TUMBLEDRY": "TUMBLE DRY",
    "DRYCLEAN": "DRY CLEAN",

    "DRYFLAT": "DRY FLAT",
    "LINEDRY": "LINE DRY",

    "DO NOTBLEACH": "DO NOT BLEACH",

    # Iron
    "MEOIUM": "MEDIUM",
    "MEDlUM": "MEDIUM",
    "MED1UM": "MEDIUM",
    "MEDIOM": "MEDIUM",

    "L0W": "LOW",
    "H1GH": "HIGH",

    # Country
    "IND0NESIA": "INDONESIA",
    "IND0IA": "INDIA",
    "CH1NA": "CHINA",
    "ITALY": "ITALY",
    "TURKEY": "TURKEY",
    "VIETN4M": "VIETNAM"
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    text = text.upper()

    # Remove common OCR garbage characters
    text = text.replace(
        "|",
        " "
    )

    text = text.replace(
        "®",
        " "
    )

    text = text.replace(
        "©",
        " "
    )

    text = text.replace(
        "™",
        " "
    )

    # Apply corrections
    for wrong, correct in CORRECTIONS.items():

        text = text.replace(
            wrong,
            correct
        )

    # Normalize temperature
    text = re.sub(
        r"(\d+)\s*°?\s*C",
        r"\1°C",
        text
    )

    # Normalize percentage
    text = re.sub(
        r"(\d+)\s*%",
        r"\1%",
        text
    )

    # Multiple spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

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
        clipLimit=2.5,
        tileGridSize=(8, 8)
    )

    gray = clahe.apply(gray)

    # Light blur
    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    return gray


# ============================================================
# CREATE CLEAN OCR VERSION
# ============================================================

def create_clean_version(gray):

    # OTSU threshold
    _, binary = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return binary


# ============================================================
# RUN OCR
# ============================================================

def run_ocr(image):

    results = []

    configs = [
        "--psm 6",
        "--psm 11"
    ]

    for config in configs:

        try:

            text = pytesseract.image_to_string(
                image,
                config=config
            )

            if text:

                results.append(text)

        except Exception:

            pass

    return results


# ============================================================
# VALID FABRIC LINE
# ============================================================

def extract_fabric_lines(text):

    results = []

    # Example:
    # 100% COTTON
    # 70% POLYESTER
    # 30% VISCOSE
    # 100% RAYON

    percentage_matches = re.findall(
        r"(\d+)\s*%\s*([A-Z]+)",
        text
    )

    for percentage, fabric in percentage_matches:

        fabric = fabric.upper()

        if fabric in FABRICS:

            line = (
                f"{percentage}% "
                f"{fabric}"
            )

            if line not in results:

                results.append(line)


    # Denim + Cotton format
    if "DENIM" in text:

        if not any(
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

    # Hand wash
    if "HAND WASH COLD" in text:

        return "HAND WASH COLD"

    if "HAND WASH" in text:

        return "HAND WASH"

    # Machine wash cold
    if "MACHINE WASH COLD" in text:

        return "MACHINE WASH COLD"

    # Wash at temperature
    match = re.search(
        r"WASH\s+AT\s+(\d+)\s*°?\s*C",
        text
    )

    if match:

        return (
            f"WASH AT "
            f"{match.group(1)}°C"
        )

    # Wash cold
    if "WASH COLD" in text:

        return "WASH COLD"

    # Similar colours
    if "WASH WITH SIMILAR COLOURS" in text:

        return "WASH WITH SIMILAR COLOURS"

    if "WASH WITH SIMILAR COLORS" in text:

        return "WASH WITH SIMILAR COLORS"

    if "MACHINE WASH" in text:

        return "MACHINE WASH"

    if "WASH" in text:

        return "WASH"

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

    # Handle OCR mistake
    if (
        "IRON" in text
        and "MEDIUM" in text
    ):

        return "IRON MEDIUM"

    if "IRON" in text:

        return "IRON"

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

    if (
        "WASH WITH SIMILAR COLOURS"
        in text
    ):

        results.append(
            "WASH WITH SIMILAR COLOURS"
        )

    if (
        "WASH WITH SIMILAR COLORS"
        in text
    ):

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

        valid_countries = [
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

        if country in valid_countries:

            return (
                f"MADE IN {country}"
            )

    return None


# ============================================================
# FINAL STRUCTURED OCR
# ============================================================

def extract_text(image):

    # --------------------------------------------------------
    # PREPROCESS
    # --------------------------------------------------------

    gray = preprocess_image(
        image
    )

    binary = create_clean_version(
        gray
    )


    # --------------------------------------------------------
    # OCR
    # --------------------------------------------------------

    raw_results = []

    raw_results.extend(
        run_ocr(gray)
    )

    raw_results.extend(
        run_ocr(binary)
    )


    # --------------------------------------------------------
    # COMBINE RAW OCR ONLY FOR SEARCHING
    # --------------------------------------------------------

    combined = "\n".join(
        raw_results
    )

    combined = normalize_text(
        combined
    )


    # --------------------------------------------------------
    # EXTRACT ONLY VALID INFORMATION
    # --------------------------------------------------------

    fabric_lines = extract_fabric_lines(
        combined
    )

    washing = extract_washing(
        combined
    )

    bleaching = extract_bleaching(
        combined
    )

    drying = extract_drying(
        combined
    )

    ironing = extract_ironing(
        combined
    )

    cleaning = extract_cleaning(
        combined
    )

    special = extract_special(
        combined
    )

    country = extract_country(
        combined
    )


    # --------------------------------------------------------
    # BUILD FINAL OUTPUT
    # --------------------------------------------------------

    final_lines = []


    # Fabric
    for fabric in fabric_lines:

        if fabric not in final_lines:

            final_lines.append(
                fabric
            )


    # Washing
    if washing:

        final_lines.append(
            washing
        )


    # Bleaching
    if bleaching:

        final_lines.append(
            bleaching
        )


    # Drying
    if drying:

        final_lines.append(
            drying
        )


    # Ironing
    if ironing:

        final_lines.append(
            ironing
        )


    # Cleaning
    if cleaning:

        final_lines.append(
            cleaning
        )


    # Special
    for item in special:

        if item not in final_lines:

            final_lines.append(
                item
            )


    # Country
    if country:

        final_lines.append(
            country
        )


    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    cleaned = []

    for line in final_lines:

        line = normalize_text(
            line
        )

        if line and line not in cleaned:

            cleaned.append(
                line
            )


    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    return "\n".join(
        cleaned
    )
