import re
import streamlit as st
from PIL import Image

from ocr import extract_text
from symbol_detection import detect_symbols


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI-Powered Clothing Care Label Assistant",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 36px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 8px;
}

.main-description {
    color: #b8c0cc;
    font-size: 16px;
    margin-bottom: 25px;
}

/* Main containers */

.info-container {
    background: #151922;
    border: 1px solid #303746;
    border-radius: 14px;
    padding: 22px;
    margin-top: 15px;
    margin-bottom: 25px;
}

/* Section titles */

.section-title {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 18px;
}

/* Fabric */

.fabric-card {
    background: #202632;
    border-left: 5px solid #38bdf8;
    border-radius: 10px;
    padding: 18px;
    color: #ffffff;
    font-size: 18px;
}

/* Care instruction cards */

.care-card {
    background: #202632;
    border-left: 5px solid #4da3ff;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 10px 0;
    color: #ffffff;
    font-size: 16px;
}

.bleach-card {
    border-left-color: #ff6b6b;
}

.drying-card {
    border-left-color: #f5b642;
}

.ironing-card {
    border-left-color: #a78bfa;
}

.cleaning-card {
    border-left-color: #4ade80;
}

/* Symbol cards */

.symbol-card {
    background: #202632;
    border: 1px solid #394354;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 10px 0;
    color: #ffffff;
    font-size: 16px;
}

/* Alert cards */

.alert-card {
    background: #2a2220;
    border-left: 5px solid #ff9f43;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 10px 0;
    color: #ffffff;
    font-size: 16px;
}

/* Final report */

.report-card {
    background: #171c26;
    border: 1px solid #3b4557;
    border-radius: 14px;
    padding: 22px;
    color: #ffffff;
    line-height: 1.8;
    font-size: 16px;
}

.report-heading {
    color: #ffffff;
    font-size: 19px;
    font-weight: 700;
    margin-top: 15px;
    margin-bottom: 5px;
}

/* OCR box */

.ocr-container {
    background: #151922;
    border: 1px solid #303746;
    border-radius: 14px;
    padding: 22px;
    margin-top: 15px;
    margin-bottom: 25px;
}

/* Upload area */

.upload-container {
    background: #151922;
    border: 1px solid #303746;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">AI-Powered Clothing Care Label Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-description">'
    'Upload a clothing care label image to extract fabric information '
    'and understand the recommended care instructions.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# FABRIC DETECTION
# ============================================================

def detect_fabric(text):

    fabric_names = [
        "COTTON",
        "POLYESTER",
        "VISCOSE",
        "RAYON",
        "SILK",
        "WOOL",
        "NYLON",
        "LINEN",
        "ELASTANE",
        "ACRYLIC",
        "DENIM",
        "SPANDEX"
    ]

    text_upper = text.upper()

    detected = []

    # --------------------------------------------------------
    # Detect percentage + fabric
    # Example: 98% COTTON
    # --------------------------------------------------------

    percentage_matches = re.findall(
        r"(\d+)\s*%\s*([A-Z]+)",
        text_upper
    )

    for percentage, fabric in percentage_matches:

        if fabric in fabric_names:

            result = f"{percentage}% {fabric.title()}"

            if result not in detected:
                detected.append(result)

    # --------------------------------------------------------
    # Detect fabric names without percentage
    # --------------------------------------------------------

    for fabric in fabric_names:

        if fabric in text_upper:

            already_detected = False

            for item in detected:

                if fabric.title() in item:
                    already_detected = True
                    break

            if not already_detected:

                detected.append(fabric.title())

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    final_detected = []

    for item in detected:

        if item not in final_detected:
            final_detected.append(item)

    if not final_detected:

        return "Fabric composition was not detected."

    return " + ".join(final_detected)


# ============================================================
# WASHING ANALYSIS
# ============================================================

def analyze_washing(text):

    text = text.upper()

    if "HAND WASH" in text:

        if "COLD" in text:
            return "Hand wash with cold water"

        return "Hand wash gently"

    if "MACHINE WASH COLD" in text:

        return "Machine wash with cold water"

    if "WASH AT 40" in text:

        return "Wash at 40°C"

    if "WASH AT 30" in text:

        return "Wash at 30°C"

    if "MACHINE WASH" in text:

        return "Machine wash"

    if "WASH" in text:

        return "Follow the washing instructions on the label"

    return "Washing instruction not detected"


# ============================================================
# BLEACH ANALYSIS
# ============================================================

def analyze_bleach(text):

    text = text.upper()

    if "DO NOT BLEACH" in text:

        return "Do not use bleach"

    if "NO BLEACH" in text:

        return "Do not use bleach"

    if "BLEACH" in text:

        return "Check bleach instructions carefully"

    return "Bleaching instruction not detected"


# ============================================================
# DRYING ANALYSIS
# ============================================================

def analyze_drying(text):

    text = text.upper()

    if "DO NOT TUMBLE DRY" in text:

        return "Do not tumble dry"

    if "TUMBLE DRY LOW" in text:

        return "Tumble dry using low heat"

    if "TUMBLE DRY MEDIUM" in text:

        return "Tumble dry using medium heat"

    if "TUMBLE DRY HIGH" in text:

        return "Tumble dry using high heat"

    if "TUMBLE DRY" in text:

        return "Tumble dry according to label instructions"

    if "DRY FLAT" in text:

        return "Dry flat"

    if "LINE DRY" in text:

        return "Line dry"

    return "Drying instruction not detected"


# ============================================================
# IRONING ANALYSIS
# ============================================================

def analyze_ironing(text):

    text = text.upper()

    if "DO NOT IRON" in text:

        return "Do not iron"

    if "IRON LOW" in text:

        return "Iron at low temperature"

    if "IRON MEDIUM" in text:

        return "Iron at medium temperature"

    if "IRON HIGH" in text:

        return "Iron at high temperature"

    if "IRON" in text:

        return "Iron according to label instructions"

    return "Ironing instruction not detected"


# ============================================================
# DRY CLEANING ANALYSIS
# ============================================================

def analyze_dry_cleaning(text):

    text = text.upper()

    if "DO NOT DRY CLEAN" in text:

        return "Do not dry clean"

    if "DRY CLEAN" in text:

        return "Dry cleaning is allowed"

    return "Dry cleaning instruction not detected"


# ============================================================
# CARE ALERTS
# ============================================================

def generate_alerts(
    washing,
    bleach,
    drying,
    ironing,
    dry_cleaning
):

    alerts = []

    if "Do not use bleach" in bleach:

        alerts.append(
            "Avoid using bleach."
        )

    if "low heat" in drying.lower():

        alerts.append(
            "Use low heat while tumble drying."
        )

    if "medium heat" in drying.lower():

        alerts.append(
            "Use medium heat while tumble drying."
        )

    if "high heat" in drying.lower():

        alerts.append(
            "Use high heat while tumble drying."
        )

    if "Do not tumble dry" in drying:

        alerts.append(
            "Do not use a tumble dryer."
        )

    if "low temperature" in ironing.lower():

        alerts.append(
            "Use low temperature while ironing."
        )

    if "medium temperature" in ironing.lower():

        alerts.append(
            "Use medium temperature while ironing."
        )

    if "high temperature" in ironing.lower():

        alerts.append(
            "Use high temperature while ironing."
        )

    if "Do not iron" in ironing:

        alerts.append(
            "Do not iron the garment."
        )

    if "Dry flat" in drying:

        alerts.append(
            "Dry the garment flat."
        )

    if "Line dry" in drying:

        alerts.append(
            "Line dry the garment."
        )

    if not alerts:

        alerts.append(
            "Follow all care instructions shown on the label."
        )

    return alerts


# ============================================================
# FINAL REPORT TEXT
# ============================================================

def create_report(
    fabric,
    washing,
    bleach,
    drying,
    ironing,
    dry_cleaning,
    alerts
):

    report = f"""
AI-POWERED CLOTHING CARE LABEL ASSISTANT

========================================
FABRIC INFORMATION
========================================
{fabric}

========================================
WASHING
========================================
{washing}

========================================
BLEACHING
========================================
{bleach}

========================================
DRYING
========================================
{drying}

========================================
IRONING
========================================
{ironing}

========================================
DRY CLEANING
========================================
{dry_cleaning}

========================================
IMPORTANT CARE ALERTS
========================================

"""

    for alert in alerts:

        report += f"- {alert}\n"

    report += """
========================================
END OF REPORT
========================================
"""

    return report.strip()


# ============================================================
# IMAGE UPLOAD
# ============================================================

st.markdown(
    '<div class="upload-container">',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload Clothing Care Label Image",
    type=["jpg", "jpeg", "png"]
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# PROCESS IMAGE
# ============================================================

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    # --------------------------------------------------------
    # Uploaded Image
    # --------------------------------------------------------

    st.subheader("Uploaded Image")

    st.image(
        image,
        width=500
    )

    # --------------------------------------------------------
    # OCR
    # --------------------------------------------------------

    with st.spinner("Extracting text from image..."):

        text = extract_text(image)

    # --------------------------------------------------------
    # OCR RESULT
    # --------------------------------------------------------

    st.markdown("""
    <div class="ocr-container">

    <div class="section-title">
    Extracted Text
    </div>
    """, unsafe_allow_html=True)

    if text:

        st.text_area(
            "OCR Output",
            text,
            height=180
        )

    else:

        st.warning(
            "No readable text was detected."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # FABRIC INFORMATION
    # --------------------------------------------------------

    fabric = detect_fabric(text)

    st.markdown("""
    <div class="info-container">

    <div class="section-title">
    Fabric Information
    </div>

    <div class="fabric-card">
    """ + fabric + """
    </div>

    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # CARE ANALYSIS
    # --------------------------------------------------------

    washing = analyze_washing(text)

    bleach = analyze_bleach(text)

    drying = analyze_drying(text)

    ironing = analyze_ironing(text)

    dry_cleaning = analyze_dry_cleaning(text)

    # --------------------------------------------------------
    # CARE INSTRUCTIONS
    # --------------------------------------------------------

    st.markdown("""
    <div class="info-container">

    <div class="section-title">
    Care Instructions
    </div>

    <div class="care-card">
    <b>Washing</b><br>
    """ + washing + """
    </div>

    <div class="care-card bleach-card">
    <b>Bleaching</b><br>
    """ + bleach + """
    </div>

    <div class="care-card drying-card">
    <b>Drying</b><br>
    """ + drying + """
    </div>

    <div class="care-card ironing-card">
    <b>Ironing</b><br>
    """ + ironing + """
    </div>

    <div class="care-card cleaning-card">
    <b>Dry Cleaning</b><br>
    """ + dry_cleaning + """
    </div>

    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # CARE SYMBOL DETECTION
    # --------------------------------------------------------

    st.markdown("""
    <div class="info-container">

    <div class="section-title">
    Care Symbol Detection
    </div>
    """, unsafe_allow_html=True)

    try:

        symbols = detect_symbols(
            image,
            text
        )

        if symbols:

            for symbol in symbols:

                st.markdown(
                    f"""
                    <div class="symbol-card">
                    {symbol}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.markdown(
                """
                <div class="symbol-card">
                No care symbols detected.
                </div>
                """,
                unsafe_allow_html=True
            )

    except Exception:

        st.markdown(
            """
            <div class="symbol-card">
            Care symbol detection could not be completed.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # IMPORTANT CARE ALERTS
    # --------------------------------------------------------

    alerts = generate_alerts(
        washing,
        bleach,
        drying,
        ironing,
        dry_cleaning
    )

    st.markdown("""
    <div class="info-container">

    <div class="section-title">
    Important Care Alerts
    </div>
    """, unsafe_allow_html=True)

    for alert in alerts:

        st.markdown(
            f"""
            <div class="alert-card">
            {alert}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # FINAL REPORT TEXT
    # --------------------------------------------------------

    report = create_report(
        fabric,
        washing,
        bleach,
        drying,
        ironing,
        dry_cleaning,
        alerts
    )

    # --------------------------------------------------------
    # FINAL CARE REPORT
    # --------------------------------------------------------

    st.markdown("""
    <div class="info-container">

    <div class="section-title">
    Final Care Report
    </div>

    <div class="report-card">

    <div class="report-heading">
    Fabric Information
    </div>
    """ + fabric + """

    <div class="report-heading">
    Washing
    </div>
    """ + washing + """

    <div class="report-heading">
    Bleaching
    </div>
    """ + bleach + """

    <div class="report-heading">
    Drying
    </div>
    """ + drying + """

    <div class="report-heading">
    Ironing
    </div>
    """ + ironing + """

    <div class="report-heading">
    Dry Cleaning
    </div>
    """ + dry_cleaning + """

    <div class="report-heading">
    Care Recommendations
    </div>

    <ul>
    """ + "".join(
        f"<li>{alert}</li>"
        for alert in alerts
    ) + """
    </ul>

    </div>

    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # DOWNLOAD REPORT
    # --------------------------------------------------------

    st.download_button(
        label="Download Care Report",
        data=report,
        file_name="clothing_care_report.txt",
        mime="text/plain"
    )