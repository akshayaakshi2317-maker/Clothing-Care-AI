import pytesseract
import re

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# --------------------------------------------------
# CLEAN OCR TEXT
# --------------------------------------------------

def clean_text(text):

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        # Common OCR corrections
        line = line.replace("DONOT", "DO NOT")
        line = line.replace("IRONLOW", "IRON LOW")
        line = line.replace("WASHCOLD", "WASH COLD")
        line = line.replace("TUMBLEDRY", "TUMBLE DRY")
        line = line.replace("DRYCLEAN", "DRY CLEAN")

        # Remove extra spaces
        line = re.sub(r"\s+", " ", line)

        # Keep useful clothing-related text
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

        # Check percentage composition
        has_percentage = bool(
            re.search(r"\d+\s*%", line)
        )

        # Check useful keyword
        has_keyword = any(
            word in line.upper()
            for word in keywords
        )

        # Ignore small OCR noise
        if has_percentage or has_keyword:

            if line not in lines:
                lines.append(line)

    return "\n".join(lines)


# --------------------------------------------------
# OCR EXTRACTION
# --------------------------------------------------

def extract_text(image):

    # Convert to grayscale
    gray = ImageOps.grayscale(image)


    # Increase image size
    width, height = gray.size

    gray = gray.resize(
        (width * 2, height * 2)
    )


    # Improve contrast
    gray = ImageEnhance.Contrast(
        gray
    ).enhance(2.5)


    # Improve sharpness
    gray = ImageEnhance.Sharpness(
        gray
    ).enhance(2.0)


    # Sharpen image
    gray = gray.filter(
        ImageFilter.SHARPEN
    )


    # OCR
    text = pytesseract.image_to_string(
        gray,
        config="--psm 6"
    )


    # Clean OCR output
    text = clean_text(text)


    return text.strip()