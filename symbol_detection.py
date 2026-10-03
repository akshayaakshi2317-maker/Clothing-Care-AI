import cv2
import numpy as np


def detect_symbols(image, text=""):

    symbols = []

    # --------------------------------------------------
    # IMAGE-BASED CHECK
    # --------------------------------------------------

    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(
        gray,
        200,
        255,
        cv2.THRESH_BINARY_INV
    )

    height, width = gray.shape

    # Symbol row in the uploaded label
    y1 = int(height * 0.20)
    y2 = int(height * 0.43)

    symbol_area = binary[y1:y2, :]

    # Count dark pixels in vertical direction
    projection = np.sum(
        symbol_area > 0,
        axis=0
    )

    # Find groups of dark pixels
    groups = []
    start = None

    for x in range(width):

        if projection[x] > 2:

            if start is None:
                start = x

        else:

            if start is not None:

                if x - start > 10:
                    groups.append(
                        (start, x)
                    )

                start = None

    # --------------------------------------------------
    # OCR CROSS-CHECK
    # --------------------------------------------------

    text_upper = text.upper()

    # Washing
    if (
        "MACHINE WASH" in text_upper
        or "WASH COLD" in text_upper
        or "HAND WASH" in text_upper
    ):
        symbols.append(
            "Washing Symbol"
        )

    # Bleaching
    if (
        "DO NOT BLEACH" in text_upper
        or "NO BLEACH" in text_upper
    ):
        symbols.append(
            "Do Not Bleach Symbol"
        )

    # Tumble drying
    if (
        "TUMBLE DRY" in text_upper
        or "DO NOT TUMBLE DRY" in text_upper
    ):
        symbols.append(
            "Tumble Drying Symbol"
        )

    # Ironing
    if (
        "IRON LOW" in text_upper
        or "LOW IRON" in text_upper
        or "IRON MEDIUM" in text_upper
        or "IRON HIGH" in text_upper
        or "DO NOT IRON" in text_upper
    ):
        symbols.append(
            "Ironing Symbol"
        )

    # Dry cleaning
    if (
        "DRY CLEAN" in text_upper
        or "DO NOT DRY CLEAN" in text_upper
    ):
        symbols.append(
            "Dry Cleaning Symbol"
        )

    # Remove duplicates
    symbols = list(
        dict.fromkeys(symbols)
    )

    return symbols