import os
import re
import shutil

import cv2
import numpy as np
import pytesseract


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
# FABRIC NAMES
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
# COMMON OCR CORRECTIONS
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

    "DRYFLAT": "DRY FLAT",

    "DONOTWRING": "DO NOT WRING",

    "WASHINSIDEOUT": "WASH INSIDE OUT",

    "IRONONREVERSE": "IRON ON REVERSE"
}


# ============================================================
# CARE WORDS
# ============================================================

CARE_WORDS = [
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

    # Slight noise reduction
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

    gray = clahe.apply(gray)

    return gray


# ============================================================
# CREATE OCR VARIANTS
# ============================================================

def create_variants(gray):

    variants = []

    # Original enhanced image
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

    return variants


# ============================================================
# OCR ERROR CORRECTION
# ============================================================

def correct_ocr_text(text):

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

    return text


# ============================================================
# CHECK USEFUL LINE
# ============================================================

def useful_line(line):

    line = line.upper().strip()

    if not line:
        return False

    # Fabric percentage
    if re.search(
        r"\d+\s*%\s*[A-Z]+",
        line
    ):
        return True

    # Temperature
    if re.search(
        r"\d+\s*°?\s*C",
        line
    ):
        return True

    # Fabric names
    for fabric in FABRICS:

        if fabric in line:
            return True

    # Care words
    for word in CARE_WORDS:

        if word in line:
            return True

    return False


# ============================================================
# CLEAN SINGLE OCR LINE
# ============================================================

def clean_line(line):

    line = line.upper().strip()

    # Remove leading garbage
    line = re.sub(
        r"^[^A-Z0-9]+",
        "",
        line
    )

    # Replace unwanted punctuation
    line = line.replace(
        "|",
        " "
    )

    line = line.replace(
        ":",
        " "
    )

    line = line.replace(
        ";",
        " "
    )

    # Fix OCR corrections
    line = correct_ocr_text(
        line
    )

    # Fix percentage
    line = re.sub(
        r"(\d+)\s+%",
        r"\1%",
        line
    )

    # Fix temperature
    line = re.sub(
        r"(\d+)\s*°?\s*C\b",
        r"\1°C",
        line
    )

    # Normalize spaces
    line = re.sub(
        r"\s+",
        " ",
        line
    ).strip()

    return line


# ============================================================
# EXTRACT ONE OCR RESULT
# ============================================================

def run_single_ocr(image, config):

    try:

        result = pytesseract.image_to_string(
            image,
            config=config
        )

        return result

    except Exception:

        return ""


# ============================================================
# EXTRACT TEXT
# ============================================================

def extract_text(image):

    gray = preprocess_image(
        image
    )

    variants = create_variants(
        gray
    )

    configs = [
        "--psm 6",
        "--psm 11",
        "--psm 12"
    ]

    all_lines = []

    # --------------------------------------------------------
    # Run OCR
    # --------------------------------------------------------

    for variant in variants:

        for config in configs:

            result = run_single_ocr(
                variant,
                config
            )

            if not result:
                continue

            for raw_line in result.splitlines():

                line = clean_line(
                    raw_line
                )

                if not line:
                    continue

                if not useful_line(line):
                    continue

                if line not in all_lines:

                    all_lines.append(line)


    # --------------------------------------------------------
    # Build final clean result
    # --------------------------------------------------------

    final_lines = []

    priority_patterns = [

        # Fabric
        r"\d+\s*%\s*[A-Z]+",

        # Washing
        r"MACHINE WASH",
        r"HAND WASH",
        r"WASH AT",
        r"WASH COLD",
        r"WASH WITH",

        # Bleaching
        r"DO NOT BLEACH",
        r"NO BLEACH",

        # Drying
        r"DO NOT TUMBLE DRY",
        r"TUMBLE DRY",
        r"DRY FLAT",
        r"LINE DRY",

        # Ironing
        r"DO NOT IRON",
        r"IRON",

        # Cleaning
        r"DO NOT DRY CLEAN",
        r"DRY CLEAN",

        # Special
        r"DO NOT WRING",
        r"WRING",
        r"REVERSE",

        # Country
        r"MADE IN"
    ]


    for pattern in priority_patterns:

        for line in all_lines:

            if re.search(
                pattern,
                line
            ):

                if line not in final_lines:

                    final_lines.append(
                        line
                    )


    # --------------------------------------------------------
    # Smart duplicate removal
    # --------------------------------------------------------

    unique_lines = []

    for line in final_lines:

        normalized = re.sub(
            r"[^A-Z0-9%° ]",
            "",
            line
        )

        normalized = re.sub(
            r"\s+",
            " ",
            normalized
        ).strip()

        duplicate = False

        for existing in unique_lines:

            existing_normalized = re.sub(
                r"[^A-Z0-9%° ]",
                "",
                existing
            )

            existing_normalized = re.sub(
                r"\s+",
                " ",
                existing_normalized
            ).strip()

            if normalized == existing_normalized:

                duplicate = True
                break

        if not duplicate:

            unique_lines.append(
                line
            )


    return "\n".join(
        unique_lines
    )
