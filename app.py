import re
import streamlit as st
from PIL import Image

from ocr import extract_text
from symbol_detection import detect_symbols


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Clothing Care AI",
    page_icon="",
    layout="wide"
)


# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    color: #4b0082;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #666666;
    font-size: 17px;
    margin-bottom: 25px;
}

.box {
    padding: 18px;
    border-radius: 14px;
    margin: 12px 0;
    color: #222222;
    font-size: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.fabric {
    background: #f0e7ff;
    border-left: 7px solid #7b2cbf;
}

.wash {
    background: #e3f2fd;
    border-left: 7px solid #1976d2;
}

.bleach {
    background: #ffebee;
    border-left: 7px solid #e53935;
}

.dry {
    background: #fff3e0;
    border-left: 7px solid #fb8c00;
}

.iron {
    background: #e8f5e9;
    border-left: 7px solid #2e7d32;
}

.clean {
    background: #efebe9;
    border-left: 7px solid #795548;
}

.symbol {
    background: #f3e5f5;
    border-left: 7px solid #8e24aa;
}

.alert {
    background: #fff0f0;
    border-left: 7px solid #d32f2f;
}

.report {
    background: #e8eaf6;
    border-left: 7px solid #3949ab;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title">AI-Powered Clothing Care Label Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'OCR-based clothing care label analysis and recommendation system'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# UPLOAD
# =========================================================

st.header("Upload Clothing Care Label")

uploaded_file = st.file_uploader(
    "Choose a clothing care label image",
    type=["jpg", "jpeg", "png", "webp"]
)


# =========================================================
# MAIN PROCESS
# =========================================================

if uploaded_file:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Clothing Label",
        width="stretch"
    )

    # -----------------------------------------------------
    # OCR
    # -----------------------------------------------------

    with st.spinner("Analyzing clothing label..."):
        raw_text = extract_text(image)

    # -----------------------------------------------------
    # CLEAN DISPLAY TEXT
    # -----------------------------------------------------

    def clean_display_text(text):

        text = text.upper()

        result = []

        # Fabric
        if "DENIM" in text and "COTTON" in text:

            result.append("100% DENIM (COTTON)")

        else:

            matches = re.findall(
                r"(\d{1,3})\s*%\s*"
                r"(COTTON|POLYESTER|VISCOSE|RAYON|SILK|WOOL|"
                r"NYLON|LINEN|ELASTANE|ACRYLIC|DENIM|SPANDEX)",
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

            result.append(
                f"WASH AT {match.group(1)}°C"
            )

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
            r"MADE\s+IN\s+"
            r"(INDIA|CHINA|ITALY|UK|VIETNAM|TURKEY|"
            r"INDONESIA|BANGLADESH|PAKISTAN)",
            text
        )

        if match:

            result.append(
                "MADE IN " + match.group(1)
            )

        # Remove duplicates
        final = []

        for item in result:

            if item not in final:
                final.append(item)

        return "\n".join(final)


    text = clean_display_text(raw_text)

    upper = text.upper()


    # =====================================================
    # EXTRACTED TEXT
    # =====================================================

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


    # =====================================================
    # FABRIC INFORMATION
    # =====================================================

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


    # =====================================================
    # CARE INSTRUCTIONS
    # =====================================================

    st.header("Care Instructions")


    # Washing
    washing = "Not detected"

    match = re.search(
        r"WASH AT\s*(\d+)\s*°?\s*C",
        upper
    )

    if match:

        washing = (
            f"Wash at {match.group(1)}°C"
        )

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


    # Display cards
    st.markdown(
        f'<div class="box wash">'
        f'<b>Washing</b><br>{washing}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="box bleach">'
        f'<b>Bleaching</b><br>{bleaching}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="box dry">'
        f'<b>Drying</b><br>{drying}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="box iron">'
        f'<b>Ironing</b><br>{ironing}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="box clean">'
        f'<b>Dry Cleaning</b><br>{cleaning}'
        f'</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # SYMBOL DETECTION
    # =====================================================

    st.header("Care Symbol Detection")

    symbols = detect_symbols(
        image,
        text
    )

    if symbols:

        for symbol in symbols:

            st.markdown(
                f'<div class="box symbol">'
                f'{symbol}'
                f'</div>',
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No care symbols detected."
        )


    # =====================================================
    # ALERTS
    # =====================================================

    st.header("Important Care Alerts")

    alerts = []


    if "DO NOT BLEACH" in upper:

        alerts.append(
            "Avoid using bleach."
        )


    if "TUMBLE DRY LOW" in upper:

        alerts.append(
            "Use low heat while tumble drying."
        )

    elif "TUMBLE DRY MEDIUM" in upper:

        alerts.append(
            "Use medium heat while tumble drying."
        )

    elif "TUMBLE DRY HIGH" in upper:

        alerts.append(
            "Use high heat while tumble drying."
        )


    if "IRON LOW" in upper:

        alerts.append(
            "Use low temperature while ironing."
        )

    elif "IRON MEDIUM" in upper:

        alerts.append(
            "Use medium temperature while ironing."
        )

    elif "IRON HIGH" in upper:

        alerts.append(
            "Use high temperature while ironing."
        )


    if "DO NOT IRON" in upper:

        alerts.append(
            "Do not iron the garment."
        )


    if "DO NOT TUMBLE DRY" in upper:

        alerts.append(
            "Avoid tumble drying."
        )


    if alerts:

        for alert in alerts:

            st.markdown(
                f'<div class="box alert">'
                f'{alert}'
                f'</div>',
                unsafe_allow_html=True
            )

    else:

        st.success(
            "No major care alerts detected."
        )


    # =====================================================
    # FINAL REPORT
    # =====================================================

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


    st.markdown(
        f'<div class="box report">'
        f'<pre>{report}</pre>'
        f'</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # DOWNLOAD
    # =====================================================

    st.download_button(
        "Download Care Report",
        report,
        file_name="clothing_care_report.txt",
        mime="text/plain"
    )
