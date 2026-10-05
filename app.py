import re
import streamlit as st
from PIL import Image

from ocr import extract_text
from symbol_detection import detect_symbols


st.set_page_config(
    page_title="Clothing Care AI",
    page_icon="",
    layout="wide"
)

# ---------------- CSS ----------------

st.markdown("""
<style>
.box {
    padding: 15px;
    border-radius: 12px;
    margin: 10px 0;
    color: #111111;
    background-color: #f2f2f2;
    border-left: 5px solid #555555;
}

.fabric {
    background-color: #eee8ff;
    border-left-color: #7048c8;
}

.wash {
    background-color: #e8f3ff;
    border-left-color: #1683ff;
}

.bleach {
    background-color: #ffecec;
    border-left-color: #e63946;
}

.dry {
    background-color: #fff1e4;
    border-left-color: #ff851b;
}

.iron {
    background-color: #e5faf4;
    border-left-color: #20a080;
}

.clean {
    background-color: #f5ece8;
    border-left-color: #795548;
}

.alert {
    background-color: #ffecec;
    border-left-color: #e63946;
}
</style>
""", unsafe_allow_html=True)


# ---------------- CLEAN DISPLAY TEXT ----------------

def clean_display_text(text):

    text = text.upper()

    result = []

    # Fabric
    if "DENIM" in text and "COTTON" in text:
        result.append("100% DENIM (COTTON)")
    else:
        matches = re.findall(
            r"(\d{1,3})\s*%\s*(COTTON|POLYESTER|VISCOSE|RAYON|SILK|WOOL|NYLON|LINEN|ELASTANE|ACRYLIC|DENIM|SPANDEX)",
            text
        )

        for percentage, fabric in matches:
            line = f"{percentage}% {fabric}"

            if line not in result:
                result.append(line)

    # Washing
    match = re.search(
        r"WASH\s*AT\s*(\d+)\s*°?\s*C",
        text
    )

    if match:
        result.append(f"WASH AT {match.group(1)}°C")

    elif "MACHINE WASH COLD" in text:
        result.append("MACHINE WASH COLD")

    elif "HAND WASH COLD" in text:
        result.append("HAND WASH COLD")

    elif "HAND WASH" in text:
        result.append("HAND WASH")

    # Bleaching
    if "DO NOT BLEACH" in text:
        result.append("DO NOT BLEACH")

    elif "NO BLEACH" in text:
        result.append("NO BLEACH")

    # Drying
    if "DO NOT TUMBLE DRY" in text:
        result.append("DO NOT TUMBLE DRY")

    elif "TUMBLE DRY LOW" in text:
        result.append("TUMBLE DRY LOW")

    elif "TUMBLE DRY MEDIUM" in text:
        result.append("TUMBLE DRY MEDIUM")

    elif "TUMBLE DRY HIGH" in text:
        result.append("TUMBLE DRY HIGH")

    elif "DRY FLAT" in text:
        result.append("DRY FLAT")

    elif "LINE DRY" in text:
        result.append("LINE DRY")

    # Ironing
    if "DO NOT IRON" in text:
        result.append("DO NOT IRON")

    elif "IRON LOW" in text:
        result.append("IRON LOW")

    elif "IRON MEDIUM" in text:
        result.append("IRON MEDIUM")

    elif "IRON HIGH" in text:
        result.append("IRON HIGH")

    # Dry cleaning
    if "DO NOT DRY CLEAN" in text:
        result.append("DO NOT DRY CLEAN")

    elif "DRY CLEAN" in text:
        result.append("DRY CLEAN")

    # Country
    match = re.search(
        r"MADE\s+IN\s+(INDIA|CHINA|ITALY|UK|VIETNAM|TURKEY|INDONESIA|BANGLADESH|PAKISTAN)",
        text
    )

    if match:
        result.append("MADE IN " + match.group(1))

    # Remove duplicates
    final = []

    for item in result:
        if item not in final:
            final.append(item)

    return "\n".join(final)


# ---------------- TITLE ----------------

st.title("AI-Powered Clothing Care Label Assistant")

st.write(
    "Upload a clothing care label image to extract and analyze "
    "fabric and care instructions."
)


# ---------------- UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Upload Clothing Care Label",
    type=["jpg", "jpeg", "png", "webp"]
)


if uploaded_file:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Clothing Label",
        width="stretch"
    )

    # ---------------- OCR ----------------

    with st.spinner("Analyzing clothing label..."):
        raw_text = extract_text(image)

    # Clean output for display
    text = clean_display_text(raw_text)

    # ---------------- EXTRACTED TEXT ----------------

    st.header("Extracted Text")

    if text:

        st.text_area(
            "Detected Information",
            text,
            height=180
        )

    else:

        st.warning(
            "No readable clothing-care information detected."
        )

    upper = text.upper()

    # ---------------- FABRIC ----------------

    st.header("Fabric Information")

    fabric_lines = []

    for line in text.splitlines():

        if "%" in line or "DENIM" in line:

            if line not in fabric_lines:
                fabric_lines.append(line)

    if fabric_lines:

        st.markdown(
            '<div class="box fabric">'
            '<b>Fabric Composition</b><br><br>'
            + "<br>".join(fabric_lines)
            + "</div>",
            unsafe_allow_html=True
        )

    else:

        st.info("Fabric composition not detected.")


    # ---------------- CARE INSTRUCTIONS ----------------

    st.header("Care Instructions")

    # Washing
    washing = "Not detected"

    match = re.search(
        r"WASH AT\s*(\d+)\s*°?\s*C",
        upper
    )

    if match:
        washing = f"Wash at {match.group(1)}°C"

    elif "MACHINE WASH COLD" in upper:
        washing = "Machine wash with cold water"

    elif "HAND WASH COLD" in upper:
        washing = "Hand wash with cold water"

    elif "HAND WASH" in upper:
        washing = "Hand wash"


    # Bleaching
    if "DO NOT BLEACH" in upper:
        bleaching = "Do not use bleach"
    elif "NO BLEACH" in upper:
        bleaching = "Do not use bleach"
    else:
        bleaching = "Not detected"


    # Drying
    if "DO NOT TUMBLE DRY" in upper:
        drying = "Do not tumble dry"

    elif "TUMBLE DRY LOW" in upper:
        drying = "Tumble dry using low heat"

    elif "TUMBLE DRY MEDIUM" in upper:
        drying = "Tumble dry using medium heat"

    elif "TUMBLE DRY HIGH" in upper:
        drying = "Tumble dry using high heat"

    elif "DRY FLAT" in upper:
        drying = "Dry flat"

    elif "LINE DRY" in upper:
        drying = "Line dry"

    else:
        drying = "Not detected"


    # Ironing
    if "DO NOT IRON" in upper:
        ironing = "Do not iron"

    elif "IRON LOW" in upper:
        ironing = "Iron at low temperature"

    elif "IRON MEDIUM" in upper:
        ironing = "Iron at medium temperature"

    elif "IRON HIGH" in upper:
        ironing = "Iron at high temperature"

    else:
        ironing = "Not detected"


    # Dry cleaning
    if "DO NOT DRY CLEAN" in upper:
        cleaning = "Do not dry clean"

    elif "DRY CLEAN" in upper:
        cleaning = "Dry cleaning is allowed"

    else:
        cleaning = "Not detected"


    st.markdown(
        f'<div class="box wash"><b>Washing</b><br>{washing}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="box bleach"><b>Bleaching</b><br>{bleaching}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="box dry"><b>Drying</b><br>{drying}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="box iron"><b>Ironing</b><br>{ironing}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="box clean"><b>Dry Cleaning</b><br>{cleaning}</div>',
        unsafe_allow_html=True
    )


    # ---------------- SYMBOL DETECTION ----------------

    st.header("Care Symbol Detection")

    symbols = detect_symbols(image, text)

    if symbols:

        for symbol in symbols:

            st.markdown(
                f'<div class="box">{symbol}</div>',
                unsafe_allow_html=True
            )

    else:

        st.info("No care symbols detected.")


    # ---------------- ALERTS ----------------

    st.header("Important Care Alerts")

    alerts = []

    if "DO NOT BLEACH" in upper:
        alerts.append("Avoid using bleach.")

    if "TUMBLE DRY LOW" in upper:
        alerts.append("Use low heat while tumble drying.")

    elif "TUMBLE DRY MEDIUM" in upper:
        alerts.append("Use medium heat while tumble drying.")

    elif "TUMBLE DRY HIGH" in upper:
        alerts.append("Use high heat while tumble drying.")

    if "IRON LOW" in upper:
        alerts.append("Use low temperature while ironing.")

    elif "IRON MEDIUM" in upper:
        alerts.append("Use medium temperature while ironing.")

    elif "IRON HIGH" in upper:
        alerts.append("Use high temperature while ironing.")

    if "DO NOT IRON" in upper:
        alerts.append("Do not iron the garment.")

    if "DO NOT TUMBLE DRY" in upper:
        alerts.append("Avoid tumble drying.")


    if alerts:

        for alert in alerts:

            st.markdown(
                f'<div class="box alert">{alert}</div>',
                unsafe_allow_html=True
            )

    else:

        st.success("No major care alerts detected.")


    # ---------------- FINAL REPORT ----------------

    st.header("Final Care Report")

    report = f"""AI-POWERED CLOTHING CARE LABEL ASSISTANT

FABRIC INFORMATION
{chr(10).join(fabric_lines) if fabric_lines else "Not detected"}

CARE INSTRUCTIONS
Washing: {washing}
Bleaching: {bleaching}
Drying: {drying}
Ironing: {ironing}
Dry Cleaning: {cleaning}

CARE SYMBOLS
{chr(10).join(symbols) if symbols else "Not detected"}

IMPORTANT CARE ALERTS
{chr(10).join("- " + alert for alert in alerts) if alerts else "No major alerts detected."}
"""

    st.text_area(
        "Report",
        report,
        height=300
    )

    st.download_button(
        "Download Care Report",
        report,
        file_name="clothing_care_report.txt",
        mime="text/plain"
    )
