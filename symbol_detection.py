import re


# ============================================================
# CARE SYMBOL DETECTION
# ============================================================

def detect_symbols(image, text=""):

    text = text.upper()

    symbols = []


    # ========================================================
    # WASHING
    # ========================================================

    if (
        "WASH" in text
        or "MACHINE WASH" in text
        or "HAND WASH" in text
        or "WASH AT" in text
    ):

        symbols.append(
            "Washing Symbol"
        )


    # ========================================================
    # BLEACH
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
    # TUMBLE DRY
    # ========================================================

    if (
        "TUMBLE DRY" in text
        or "DO NOT TUMBLE DRY" in text
    ):

        symbols.append(
            "Tumble Drying Symbol"
        )


    # ========================================================
    # DRY FLAT
    # ========================================================

    if "DRY FLAT" in text:

        symbols.append(
            "Dry Flat Symbol"
        )


    # ========================================================
    # LINE DRY
    # ========================================================

    if "LINE DRY" in text:

        symbols.append(
            "Line Dry Symbol"
        )


    # ========================================================
    # IRON
    # ========================================================

    if (
        "IRON" in text
        or "DO NOT IRON" in text
    ):

        symbols.append(
            "Ironing Symbol"
        )


    # ========================================================
    # DRY CLEAN
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

    result = []

    for symbol in symbols:

        if symbol not in result:

            result.append(
                symbol
            )

    return result
