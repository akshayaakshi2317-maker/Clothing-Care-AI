import streamlit as st
from PIL import Image

from ocr import extract_text
from symbol_detection import detect_symbols


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI-Powered Clothing Care Label Assistant",
    page_icon="",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #666666;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    .info-box {
        padding: 18px;
        border-radius: 14px;
        margin-bottom: 15px;
        border: 1px solid #dddddd;
        background-color: #f8f9fa;
    }

    .fabric-box {
        padding: 20px;
        border-radius: 14px;
        border-left: 6px solid #6f42c1;
        background-color: #f3efff;
        margin-bottom: 15px;
    }

    .wash-box {
        padding: 18px;
        border-radius: 14px;
        border-left: 6px solid #007bff;
        background-color: #eef6ff;
        margin-bottom: 12px;
    }

    .bleach-box {
        padding: 18px;
        border-radius: 14px;
        border-left: 6px solid #dc3545;
        background-color: #fff0f1;
        margin-bottom: 12px;
    }

    .dry-box {
        padding: 18px;
        border-radius: 14px;
        border-left: 6px solid #fd7e14;
        background-color: #fff5ec;
        margin-bottom: 12px;
    }

    .iron-box {
        padding: 18px;
        border-radius: 14px;
        border-left: 6px solid #20c997;
        background-color: #edfff9;
        margin-bottom: 12px;
    }

    .clean-box {
        padding: 18px;
        border-radius: 14px;
        border-left: 6px solid #795548;
        background-color: #f8f1ee;
        margin-bottom: 12px;
    }

    .symbol-box {
        padding: 16px;
        border-radius: 12px;
        background-color: #f4f4f4;
        border: 1px solid #dddddd;
        margin-bottom: 10px;
    }

    .alert-box {
        padding: 18px;
        border-radius: 14px;
        border-left: 6px solid #dc3545;
        background-color: #fff3f3;
        margin-bottom: 12px;
    }

    .report-box {
        padding: 22px;
        border-radius: 15px;
        background-color: #f8f9fa;
        border: 1px solid #dddddd;
        line-height: 1.7;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">AI-Powered Clothing Care Label Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">OCR-based clothing label analysis and care recommendation system</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Project Information")

    st.write(
        "Upload a clothing care label image. "
        "The system extracts the text and identifies "
        "fabric composition, washing, bleaching, drying, "
        "ironing and dry-cleaning instructions."
    )

    st.divider()

    st.write("Technologies")

    st.write(
        "Python\n\n"
        "Streamlit\n\n"
        "Tesseract OCR\n\n"
        "OpenCV\n\n"
        "NumPy\n\n"
        "Pillow"
    )


# ============================================================
# IMAGE UPLOAD
# ============================================================

st.markdown(
    '<div class="section-title">Upload Clothing Care Label</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose a clothing care label image",
    type=["jpg", "jpeg", "png", "webp"]
)


# ============================================================
# MAIN PROCESSING
# ============================================================

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    )

    image = image.convert("RGB")


    # --------------------------------------------------------
    # DISPLAY IMAGE
    # --------------------------------------------------------

    col1, col2 = st.columns(
        [1, 1]
    )

    with col1:

        st.image(
            image,
            caption="Uploaded Clothing Label",
            width="stretch"
        )


    # --------------------------------------------------------
    # OCR
    # --------------------------------------------------------

    with st.spinner("Analyzing clothing label..."):

        text = extract_text(
            image
        )


    # ========================================================
    # EXTRACTED TEXT
    # ========================================================

    st.markdown(
        '<div class="section-title">Extracted Text</div>',
        unsafe_allow_html=True
    )

    if text:

        st.text_area(
            "OCR Result",
            text,
            height=180
        )

    else:

        st.warning(
            "No readable clothing-care information was detected."
        )


    # ========================================================
    # CARE SYMBOL DETECTION
    # ========================================================

    symbols = detect_symbols(
        image,
        text
    )


    # ========================================================
    # FABRIC INFORMATION
    # ========================================================

    fabric_lines = []

    for line in text.splitlines():

        line = line.strip()

        upper_line = line.upper()

        if (
            "%"
            in upper_line
            and any(
                fabric in upper_line
                for fabric in [
                    "COTTON",
                    "POLYESTER",
                    "RAYON",
                    "VISCOSE",
                    "SILK",
                    "WOOL",
                    "NYLON",
                    "LINEN",
                    "ELASTANE",
                    "ACRYLIC",
                    "DENIM",
                    "SPANDEX"
                ]
            )
        ):

            if line not in fabric_lines:

                fabric_lines.append(
                    line
                )


    # ========================================================
    # FALLBACK FOR DENIM (COTTON)
    # ========================================================

    if (
        "DENIM (COTTON)"
        in text.upper()
        and not fabric_lines
    ):

        fabric_lines.append(
            "100% DENIM (COTTON)"
        )


    # ========================================================
    # CARE INSTRUCTION EXTRACTION
    # ========================================================

    upper_text = text.upper()


    # --------------------------------------------------------
    # WASHING
    # --------------------------------------------------------

    washing = "Washing instruction not detected"

    if "WASH AT" in upper_text:

        import re

        match = re.search(
            r"WASH\s+AT\s+(\d+)\s*°?\s*C",
            upper_text
        )

        if match:

            washing = (
                "Wash at "
                + match.group(1)
                + "°C"
            )

    elif "MACHINE WASH COLD" in upper_text:

        washing = "Machine wash with cold water"

    elif "HAND WASH COLD" in upper_text:

        washing = "Hand wash with cold water"

    elif "HAND WASH" in upper_text:

        washing = "Hand wash"

    elif "MACHINE WASH" in upper_text:

        washing = "Machine wash"


    # --------------------------------------------------------
    # BLEACHING
    # --------------------------------------------------------

    bleaching = "Bleaching instruction not detected"

    if "DO NOT BLEACH" in upper_text:

        bleaching = "Do not use bleach"

    elif "NO BLEACH" in upper_text:

        bleaching = "Do not use bleach"


    # --------------------------------------------------------
    # DRYING
    # --------------------------------------------------------

    drying = "Drying instruction not detected"

    if "DO NOT TUMBLE DRY" in upper_text:

        drying = "Do not tumble dry"

    elif "TUMBLE DRY LOW" in upper_text:

        drying = "Tumble dry using low heat"

    elif "TUMBLE DRY MEDIUM" in upper_text:

        drying = "Tumble dry using medium heat"

    elif "TUMBLE DRY HIGH" in upper_text:

        drying = "Tumble dry using high heat"

    elif "DRY FLAT" in upper_text:

        drying = "Dry flat"

    elif "LINE DRY" in upper_text:

        drying = "Line dry"

    elif "TUMBLE DRY" in upper_text:

        drying = "Tumble dry"


    # --------------------------------------------------------
    # IRONING
    # --------------------------------------------------------

    ironing = "Ironing instruction not detected"

    if "DO NOT IRON" in upper_text:

        ironing = "Do not iron"

    elif "IRON LOW" in upper_text:

        ironing = "Iron at low temperature"

    elif "IRON MEDIUM" in upper_text:

        ironing = "Iron at medium temperature"

    elif "IRON HIGH" in upper_text:

        ironing = "Iron at high temperature"

    elif "IRON ON REVERSE" in upper_text:

        ironing = "Iron on reverse side"

    elif "IRON" in upper_text:

        ironing = "Iron according to label instructions"


    # --------------------------------------------------------
    # DRY CLEANING
    # --------------------------------------------------------

    dry_cleaning = "Dry-cleaning instruction not detected"

    if "DO NOT DRY CLEAN" in upper_text:

        dry_cleaning = "Do not dry clean"

    elif "DRY CLEAN" in upper_text:

        dry_cleaning = "Dry cleaning is allowed"


    # ========================================================
    # CARE INSTRUCTIONS DISPLAY
    # ========================================================

    st.markdown(
        '<div class="section-title">Care Instructions</div>',
        unsafe_allow_html=True
    )


    # Washing
    st.markdown(
        f"""
        <div class="wash-box">
        <b>Washing</b><br>
        {washing}
        </div>
        """,
        unsafe_allow_html=True
    )


    # Bleaching
    st.markdown(
        f"""
        <div class="bleach-box">
        <b>Bleaching</b><br>
        {bleaching}
        </div>
        """,
        unsafe_allow_html=True
    )


    # Drying
    st.markdown(
        f"""
        <div class="dry-box">
        <b>Drying</b><br>
        {drying}
        </div>
        """,
        unsafe_allow_html=True
    )


    # Ironing
    st.markdown(
        f"""
        <div class="iron-box">
        <b>Ironing</b><br>
        {ironing}
        </div>
        """,
        unsafe_allow_html=True
    )


    # Dry Cleaning
    st.markdown(
        f"""
        <div class="clean-box">
        <b>Dry Cleaning</b><br>
        {dry_cleaning}
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # FABRIC INFORMATION DISPLAY
    # ========================================================

    st.markdown(
        '<div class="section-title">Fabric Information</div>',
        unsafe_allow_html=True
    )

    if fabric_lines:

        fabric_text = "<br>".join(
            fabric_lines
        )

        st.markdown(
            f"""
            <div class="fabric-box">
            <b>Fabric Composition</b><br><br>
            {fabric_text}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "Fabric composition was not detected."
        )


    # ========================================================
    # CARE SYMBOL DETECTION
    # ========================================================

    st.markdown(
        '<div class="section-title">Care Symbol Detection</div>',
        unsafe_allow_html=True
    )

    if symbols:

        for symbol in symbols:

            st.markdown(
                f"""
                <div class="symbol-box">
                <b>{symbol}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No care symbols were detected."
        )


    # ========================================================
    # IMPORTANT CARE ALERTS
    # ========================================================

    alerts = []


    if (
        "DO NOT BLEACH"
        in upper_text
    ):

        alerts.append(
            "Avoid using bleach."
        )


    if (
        "TUMBLE DRY LOW"
        in upper_text
    ):

        alerts.append(
            "Use low heat while tumble drying."
        )


    elif (
        "TUMBLE DRY MEDIUM"
        in upper_text
    ):

        alerts.append(
            "Use medium heat while tumble drying."
        )


    elif (
        "TUMBLE DRY HIGH"
        in upper_text
    ):

        alerts.append(
            "Use high heat while tumble drying."
        )


    if (
        "IRON LOW"
        in upper_text
    ):

        alerts.append(
            "Use low temperature while ironing."
        )


    elif (
        "IRON MEDIUM"
        in upper_text
    ):

        alerts.append(
            "Use medium temperature while ironing."
        )


    elif (
        "IRON HIGH"
        in upper_text
    ):

        alerts.append(
            "Use high temperature while ironing."
        )


    if (
        "DO NOT TUMBLE DRY"
        in upper_text
    ):

        alerts.append(
            "Avoid tumble drying."
        )


    if (
        "DO NOT IRON"
        in upper_text
    ):

        alerts.append(
            "Do not iron the garment."
        )


    # ========================================================
    # DISPLAY ALERTS
    # ========================================================

    st.markdown(
        '<div class="section-title">Important Care Alerts</div>',
        unsafe_allow_html=True
    )

    if alerts:

        for alert in alerts:

            st.markdown(
                f"""
                <div class="alert-box">
                {alert}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.success(
            "No major care alerts detected."
        )


    # ========================================================
    # FINAL CARE REPORT
    # ========================================================

    st.markdown(
        '<div class="section-title">Final Care Report</div>',
        unsafe_allow_html=True
    )


    report_lines = []

    report_lines.append(
        "AI-POWERED CLOTHING CARE LABEL ASSISTANT"
    )

    report_lines.append(
        ""
    )

    report_lines.append(
        "FABRIC INFORMATION"
    )

    if fabric_lines:

        for fabric in fabric_lines:

            report_lines.append(
                fabric
            )

    else:

        report_lines.append(
            "Fabric composition was not detected."
        )


    report_lines.append("")
    report_lines.append("CARE INSTRUCTIONS")

    report_lines.append(
        "Washing: " + washing
    )

    report_lines.append(
        "Bleaching: " + bleaching
    )

    report_lines.append(
        "Drying: " + drying
    )

    report_lines.append(
        "Ironing: " + ironing
    )

    report_lines.append(
        "Dry Cleaning: " + dry_cleaning
    )


    report_lines.append("")
    report_lines.append(
        "CARE SYMBOLS"
    )

    if symbols:

        for symbol in symbols:

            report_lines.append(
                symbol
            )

    else:

        report_lines.append(
            "No care symbols detected."
        )


    report_lines.append("")
    report_lines.append(
        "IMPORTANT CARE ALERTS"
    )

    if alerts:

        for alert in alerts:

            report_lines.append(
                "- " + alert
            )

    else:

        report_lines.append(
            "- No major care alerts detected."
        )


    final_report = "\n".join(
        report_lines
    )


    st.markdown(
        f"""
        <div class="report-box">
        <b>Fabric Information</b><br>
        {"<br>".join(fabric_lines) if fabric_lines else "Not detected"}
        <br><br>

        <b>Washing</b><br>
        {washing}
        <br><br>

        <b>Bleaching</b><br>
        {bleaching}
        <br><br>

        <b>Drying</b><br>
        {drying}
        <br><br>

        <b>Ironing</b><br>
        {ironing}
        <br><br>

        <b>Dry Cleaning</b><br>
        {dry_cleaning}
        <br><br>

        <b>Care Symbols</b><br>
        {"<br>".join(symbols) if symbols else "No care symbols detected"}
        <br><br>

        <b>Important Care Alerts</b><br>
        {"<br>".join("- " + a for a in alerts) if alerts else "- No major care alerts detected."}

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # DOWNLOAD REPORT
    # ========================================================

    st.markdown(
        '<div class="section-title">Download Report</div>',
        unsafe_allow_html=True
    )

    st.download_button(
        label="Download Care Report",
        data=final_report,
        file_name="clothing_care_report.txt",
        mime="text/plain"
    )
