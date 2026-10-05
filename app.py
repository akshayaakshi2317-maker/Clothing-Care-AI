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

st.markdown("""
<style>
.wash, .bleach, .dry, .iron, .clean, .fabric, .symbol, .alert, .report {
    padding: 16px;
    border-radius: 12px;
    margin: 10px 0;
    color: #111111;
}
.wash { background:#e8f3ff; border-left:5px solid #1683ff; }
.bleach { background:#ffecec; border-left:5px solid #e63946; }
.dry { background:#fff1e4; border-left:5px solid #ff851b; }
.iron { background:#e5faf4; border-left:5px solid #20c997; }
.clean { background:#f5ece8; border-left:5px solid #795548; }
.fabric { background:#eee8ff; border-left:5px solid #7048c8; }
.symbol { background:#f1f1f1; }
.alert { background:#ffecec; border-left:5px solid #e63946; }
.report { background:#f1f1f1; }
</style>
""", unsafe_allow_html=True)


st.title("AI-Powered Clothing Care Label Assistant")
st.caption("OCR-based clothing care label analysis system")

uploaded = st.file_uploader(
    "Upload Clothing Care Label",
    type=["jpg", "jpeg", "png", "webp"]
)


if uploaded:

    image = Image.open(uploaded).convert("RGB")

    st.image(
        image,
        caption="Uploaded Clothing Label",
        width="stretch"
    )

    with st.spinner("Analyzing label..."):
        text = extract_text(image)

    # ---------------- OCR RESULT ----------------

    st.header("Extracted Text")

    if text:
        st.text_area(
            "Detected Information",
            text,
            height=180
        )
    else:
        st.warning("No clothing-care information detected.")

    upper = text.upper()

    # ---------------- FABRIC ----------------

    fabric_lines = []

    for line in text.splitlines():
        if "%" in line or "DENIM" in line.upper():
            if line not in fabric_lines:
                fabric_lines.append(line)

    st.header("Fabric Information")

    if fabric_lines:
        st.markdown(
            f'<div class="fabric"><b>Fabric Composition</b><br><br>'
            + "<br>".join(fabric_lines)
            + "</div>",
            unsafe_allow_html=True
        )
    else:
        st.info("Fabric composition not detected.")

    # ---------------- CARE INSTRUCTIONS ----------------

    st.header("Care Instructions")

    washing = "Not detected"
    match = re.search(r"WASH AT\s*(\d+)\s*°?\s*C", upper)

    if match:
        washing = f"Wash at {match.group(1)}°C"
    elif "MACHINE WASH COLD" in upper:
        washing = "Machine wash with cold water"
    elif "HAND WASH" in upper:
        washing = "Hand wash"

    bleaching = (
        "Do not use bleach"
        if "DO NOT BLEACH" in upper
        else "Not detected"
    )

    if "TUMBLE DRY LOW" in upper:
        drying = "Tumble dry using low heat"
    elif "TUMBLE DRY MEDIUM" in upper:
        drying = "Tumble dry using medium heat"
    elif "TUMBLE DRY HIGH" in upper:
        drying = "Tumble dry using high heat"
    elif "DO NOT TUMBLE DRY" in upper:
        drying = "Do not tumble dry"
    else:
        drying = "Not detected"

    if "IRON LOW" in upper:
        ironing = "Iron at low temperature"
    elif "IRON MEDIUM" in upper:
        ironing = "Iron at medium temperature"
    elif "IRON HIGH" in upper:
        ironing = "Iron at high temperature"
    elif "DO NOT IRON" in upper:
        ironing = "Do not iron"
    else:
        ironing = "Not detected"

    cleaning = (
        "Do not dry clean"
        if "DO NOT DRY CLEAN" in upper
        else "Dry cleaning is allowed"
        if "DRY CLEAN" in upper
        else "Not detected"
    )

    st.markdown(
        f'<div class="wash"><b>Washing</b><br>{washing}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="bleach"><b>Bleaching</b><br>{bleaching}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="dry"><b>Drying</b><br>{drying}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="iron"><b>Ironing</b><br>{ironing}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="clean"><b>Dry Cleaning</b><br>{cleaning}</div>',
        unsafe_allow_html=True
    )

    # ---------------- SYMBOLS ----------------

    symbols = detect_symbols(image, text)

    st.header("Care Symbol Detection")

    if symbols:
        for symbol in symbols:
            st.markdown(
                f'<div class="symbol">{symbol}</div>',
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

    if "TUMBLE DRY MEDIUM" in upper:
        alerts.append("Use medium heat while tumble drying.")

    if "IRON LOW" in upper:
        alerts.append("Use low temperature while ironing.")

    if "IRON MEDIUM" in upper:
        alerts.append("Use medium temperature while ironing.")

    if "DO NOT IRON" in upper:
        alerts.append("Do not iron the garment.")

    if "DO NOT TUMBLE DRY" in upper:
        alerts.append("Avoid tumble drying.")

    if alerts:
        for alert in alerts:
            st.markdown(
                f'<div class="alert">{alert}</div>',
                unsafe_allow_html=True
            )
    else:
        st.success("No major care alerts detected.")

    # ---------------- FINAL REPORT ----------------

    st.header("Final Care Report")

    report = f"""AI-POWERED CLOTHING CARE LABEL ASSISTANT

FABRIC
{chr(10).join(fabric_lines) if fabric_lines else "Not detected"}

CARE INSTRUCTIONS
Washing: {washing}
Bleaching: {bleaching}
Drying: {drying}
Ironing: {ironing}
Dry Cleaning: {cleaning}

CARE SYMBOLS
{chr(10).join(symbols) if symbols else "Not detected"}

IMPORTANT ALERTS
{chr(10).join("- " + x for x in alerts) if alerts else "No major alerts"}
"""

    st.markdown(
        f'<div class="report"><pre>{report}</pre></div>',
        unsafe_allow_html=True
    )

    st.download_button(
        "Download Care Report",
        report,
        "clothing_care_report.txt",
        "text/plain"
    )
