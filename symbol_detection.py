def detect_symbols(image, text=""):

    text = text.upper()

    symbols = []


    if (
        "MACHINE WASH" in text
        or "HAND WASH" in text
        or "WASH AT" in text
        or "WASH COLD" in text
        or "WASH WITH" in text
        or "WASH" in text
    ):

        symbols.append(
            "Washing Symbol"
        )

    if (
        "DO NOT BLEACH" in text
        or "NO BLEACH" in text
    ):

        symbols.append(
            "Do Not Bleach Symbol"
        )


    if (
        "TUMBLE DRY" in text
        or "DO NOT TUMBLE DRY" in text
    ):

        symbols.append(
            "Tumble Drying Symbol"
        )

    if "DRY FLAT" in text:

        symbols.append(
            "Dry Flat Symbol"
        )


    if "LINE DRY" in text:

        symbols.append(
            "Line Dry Symbol"
        )


    if (
        "IRON LOW" in text
        or "IRON MEDIUM" in text
        or "IRON HIGH" in text
        or "DO NOT IRON" in text
        or "IRON ON REVERSE" in text
    ):

        symbols.append(
            "Ironing Symbol"
        )


    if (
        "DRY CLEAN" in text
        or "DO NOT DRY CLEAN" in text
    ):

        symbols.append(
            "Dry Cleaning Symbol"
        )


    result = []

    for symbol in symbols:

        if symbol not in result:

            result.append(
                symbol
            )

    return result
