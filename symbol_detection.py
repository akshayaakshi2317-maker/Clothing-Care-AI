import re


# ============================================================
# SYMBOL DETECTION USING OCR + CARE INFORMATION
# ============================================================

def detect_symbols(image, text=""):

    text = text.upper()

    symbols = []


    # ========================================================
    # WASHING SYMBOL
    # ========================================================

    if (
        "WASH" in text
        or "MACHINE" in text
        or "HAND WASH" in text
        or re.search(r"WASH AT \d+", text)
    ):

        symbols.append(
            "Washing Symbol"
        )


    # ========================================================
    # BLEACH SYMBOL
    # ========================================================

    if (
        "DO NOT BLEACH" in text
        or "NO BLEACH" in text
        or "BLEACH" in text
    ):

        symbols.append(
            "Do Not Bleach Symbol"
        )


    # ========================================================
    # TUMBLE DRY SYMBOL
    # ========================================================

    if (
        "TUMBLE DRY" in text
        or "DO NOT TUMBLE DRY" in text
    ):

        symbols.append(
            "Tumble Drying Symbol"
        )


    # ========================================================
    # DRY FLAT SYMBOL
    # ========================================================

    if "DRY FLAT" in text:

        symbols.append(
            "Dry Flat Symbol"
        )


    # ========================================================
    # LINE DRY SYMBOL
    # ========================================================

    if "LINE DRY" in text:

        symbols.append(
            "Line Dry Symbol"
        )


    # ========================================================
    # IRONING SYMBOL
    # ========================================================

    if (
        "IRON" in text
        or "DO NOT IRON" in text
    ):

        symbols.append(
            "Ironing Symbol"
        )


    # ========================================================
    # DRY CLEANING SYMBOL
    # ========================================================

    if (
        "DRY CLEAN" in text
        or "DO NOT DRY CLEAN" in text
    ):

        symbols.append(
            "Dry Cleaning Symbol"
        )


    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    final_symbols = []

    for symbol in symbols:

        if symbol not in final_symbols:

            final_symbols.append(
                symbol
            )

    return final_symbols
