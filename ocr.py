import os
import re
import shutil
import pytesseract

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


# -------------------------------
# Tesseract Configuration
# -------------------------------

tesseract_path = shutil.which("tesseract")

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

elif os.name == "nt":
    windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    if os.path.exists(windows_path):
        pytesseract.pytesseract.tesseract_cmd = windows_path


# -------------------------------
# Clean OCR Text
# -------------------------------

def clean_text(text):

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        line = line.replace("DONOT", "DO NOT")
        line = line.replace("IRONLOW", "IRON LOW")
        line = line.replace("WASHCOLD", "WASH COLD")
        line = line.replace("TUMBLEDRY", "TUMBLE DRY")
        line = line.replace("DRYCLEAN", "DRY CLEAN")

        line = re.sub(r"\s+", " ", line)

        keywords = [
            "COTTON",
            "ELASTANE",
            "POLYESTER",
            "NYLON",
            "WOOL",
            "VISCOSE",
            "LINEN",
            "SILK",
            "WASH",
            "BLEACH",
            "DRY",
            "IRON",
            "CLEAN",
            "MADE",
            "ITALY",
            "BANGLADESH",
            "CHINA",
            "INDIA",
            "VIETNAM"
        ]

        has_percentage = bool(
            re.search(r"\d+\s*%", line)
        )

        has_keyword = any(
            word in line.upper()
            for word in keywords
        )

        if has_percentage or has_keyword:

            if line not in lines:
                lines.append(line)

    return "\n".join(lines)


# -------------------------------
# OCR Extraction
# -------------------------------

def extract_text(image):

    # Convert image to grayscale
    gray = ImageOps.grayscale(image)

    # Resize image for better OCR
    width, height = gray.size

    gray = gray.resize(
        (width * 2, height * 2)
    )

    # Improve contrast
    gray = ImageEnhance.Contrast(gray).enhance(2.5)

    # Improve sharpness
    gray = ImageEnhance.Sharpness(gray).enhance(2.0)

    # Apply sharpening filter
    gray = gray.filter(ImageFilter.SHARPEN)

    # OCR
    text = pytesseract.image_to_string(
        gray,
        config="--psm 6"
    )

    # Clean OCR result
    text = clean_text(text)

    return text.strip()
