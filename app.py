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

st.markdown(
    """
<style>

.main-title {
    font-size: 38px;
    font-weight: 800;
    background: linear-gradient(
        90deg,
        #38bdf8,
        #a78bfa,
        #f472b6
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    color: #b8c0cc;
    font-size: 16px;
    margin-bottom: 25px;
}

.section {
    background: linear-gradient(
        145deg,
        #111827,
        #1e293b
    );

    border: 1px solid #475569;

    border-radius: 18px;

    padding: 24px;

    margin: 20px 0;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.25);
}

.section-title {
    color: #f8fafc;

    font-size: 25px;

    font-weight: 800;

    margin-bottom: 18px;

    padding-bottom: 10px;

    border-bottom: 1px solid #475569;
}

.fabric {
    background: linear-gradient(
        135deg,
        #075985,
        #0891b2
    );

    border: 1px solid #38bdf8;

    border-radius: 14px;

    padding: 20px;

    color: white;

    font-size: 21px;

    font-weight: 700;
}

.card {
    border-radius: 14px;

    padding: 18px 20px;

    margin: 12px 0;

    color: white;

    border: 1px solid #64748b;

    font-size: 16px;

    box-shadow:
        0 5px 15px rgba(0,0,0,0.20);
}

.washing {
    background: linear-gradient(
        135deg,
        #1e3a8a,
        #2563eb
    );
}

.bleaching {
    background: linear-gradient(
        135deg,
        #7f1d1d,
        #dc2626
    );
}

.drying {
    background: linear-gradient(
        135deg,
        #78350f,
        #d97706
    );
}

.ironing {
    background: linear-gradient(
        135deg,
        #4c1d95,
        #7c3aed
    );
}

.cleaning {
    background: linear-gradient(
        135deg,
        #14532d,
        #16a34a
    );
}

.symbol {
    background: linear-gradient(
        135deg,
        #312e81,
        #4338ca
    );

    border: 1px solid #818cf8;

    border-radius: 14px;

    padding: 16px 20px;

    margin: 10px 0;

    color: white;

    font-weight: 600;
}

.alert {
    background: linear-gradient(
        135deg,
        #78350f,
        #ea580c
    );

    border-left: 6px solid #fbbf24;

    border-radius: 14px;

    padding: 16px 20px;

    margin: 10px 0;

    color: white;

    font-weight: 600;
}

.report {
    background: linear-gradient(
        145deg,
        #0f172a,
        #1e293b
    );

    border: 1px solid #64748b;

    border-radius: 18px;

    padding: 25px;

    color: #f8fafc;

    line-height: 1.8;
}

.report-heading {
    color: #93c5fd;

    font-size: 18px;

    font-weight: 800;

    border-left: 4px solid #a78bfa;

    padding-left: 10px;

    margin-top: 15px;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    """
<div class="main-title">
AI-Powered Clothing Care Label Assistant
</div>
""",
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="subtitle">
OCR-based clothing care label analysis and intelligent care recommendations
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# FABRIC DETECTION
# ============================================================

def detect_fabric(text):

    text = text.upper()

    fabrics = [
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

    found = []

    # Percentage + fabric
    matches = re.findall(
        r"(\d+)\s*%\s*([A-Z]+)",
        text
    )

    for percentage, fabric in matches:

        if fabric in fabrics:

            value = (
                f"{percentage}% "
                f"{fabric.title()}"
            )

            if value not in found:

                found.append(value)


    # Denim without percentage
    if "DENIM" in text:

        if not any(
            "Denim" in item
            for item in found
        ):

            found.append(
                "Denim"
            )


    # Additional fabric names
    for fabric in fabrics:

        if fabric in text:

            exists = False

            for item in found:

                if fabric.title() in item:

                    exists = True
                    break

            if not exists:

                found.append(
                    fabric.title()
                )


    if not found:

        return "Fabric composition was not detected."

    return " + ".join(found)


# ============================================================
# WASHING
# ============================================================

def analyze_washing(text):

    text = text.upper()

    if "HAND WASH" in text:

        if "COLD" in text:

            return "Hand wash with cold water"

        return "Hand wash gently"

    match = re.search(
        r"WASH\s+AT\s+(\d+)\s*°?\s*C",
        text
    )

    if match:

        temperature = match.group(1)

        return (
            f"Wash at {temperature}°C"
        )

    if "MACHINE WASH COLD" in text:

        return "Machine wash with cold water"

    if "WASH COLD" in text:

        return "Wash with cold water"

    if "MACHINE WASH" in text:

        return "Machine wash"

    if "WASH WITH SIMILAR COLOURS" in text:

        return "Wash with similar colours"

    if "WASH WITH SIMILAR COLORS" in text:

        return "Wash with similar colours"

    if "WASH" in text:

        return "Follow the washing instructions on the label"

    return "Washing instruction not detected"


# ============================================================
# BLEACHING
# ============================================================

def analyze_bleach(text):

    text = text.upper()

    if (
        "DO NOT BLEACH" in text
        or "NO BLEACH" in text
    ):

        return "Do not use bleach"

    if "BLEACH" in text:

        return "Check bleach instructions carefully"

    return "Bleaching instruction not detected"


# ============================================================
# DRYING
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

    if "DRY FLAT" in text:

        return "Dry flat"

    if "LINE DRY" in text:

        return "Line dry"

    if "TUMBLE DRY" in text:

        return "Tumble dry according to label instructions"

    return "Drying instruction not detected"


# ============================================================
# IRONING
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

    if "IRON ON REVERSE" in text:

        return "Iron on the reverse side"

    if "IRON" in text:

        return "Iron according to label instructions"

    return "Ironing instruction not detected"


# ============================================================
# DRY CLEANING
# ============================================================

def analyze_cleaning(text):

    text = text.upper()

    if "DO NOT DRY CLEAN" in text:

        return "Do not dry clean"

    if "DRY CLEAN" in text:

        return "Dry cleaning is allowed"

    return "Dry cleaning instruction not detected"


# ============================================================
# SPECIAL INSTRUCTIONS
# ============================================================

def special_instructions(text):

    text = text.upper()

    results = []

    if "WASH WITH SIMILAR COLOURS" in text:

        results.append(
            "Wash with similar colours."
        )

    if "WASH WITH SIMILAR COLORS" in text:

        results.append(
            "Wash with similar colours."
        )

    if "WASH INSIDE OUT" in text:

        results.append(
            "Wash the garment inside out."
        )

    if "DO NOT WRING" in text:

        results.append(
            "Do not wring the garment."
        )

    if "IRON ON REVERSE" in text:

        results.append(
            "Iron on the reverse side."
        )

    return results


# ============================================================
# CARE ALERTS
# ============================================================

def create_alerts(
    washing,
    bleaching,
    drying,
    ironing,
    cleaning
):

    alerts = []

    if "Do not use bleach" in bleaching:

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

    return alerts


# ============================================================
# IMAGE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "Upload Clothing Care Label Image",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)


# ============================================================
# MAIN PROCESS
# ============================================================

if uploaded_file:

    image = Image.open(
        uploaded_file
    ).convert("RGB")


    # ========================================================
    # IMAGE
    # ========================================================

    st.markdown(
        """
        <div class="section">
        <div class="section-title">
        Uploaded Image
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image(
        image,
        width=500
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # OCR
    # ========================================================

    with st.spinner(
        "Analyzing clothing care label..."
    ):

        text = extract_text(
            image
        )


    # ========================================================
    # EXTRACTED TEXT
    # ========================================================

    st.markdown(
        """
        <div class="section">
        <div class="section-title">
        Extracted Text
        </div>
        """,
        unsafe_allow_html=True
    )

    if text:

        st.text_area(
            "OCR Result",
            text,
            height=220
        )

    else:

        st.warning(
            "No readable clothing care text was detected."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # ANALYSIS
    # ========================================================

    fabric = detect_fabric(
        text
    )

    washing = analyze_washing(
        text
    )

    bleaching = analyze_bleach(
        text
    )

    drying = analyze_drying(
        text
    )

    ironing = analyze_ironing(
        text
    )

    cleaning = analyze_cleaning(
        text
    )

    special = special_instructions(
        text
    )

    alerts = create_alerts(
        washing,
        bleaching,
        drying,
        ironing,
        cleaning
    )


    # ========================================================
    # FABRIC INFORMATION
    # ========================================================

    st.markdown(
        f"""
        <div class="section">

        <div class="section-title">
        Fabric Information
        </div>

        <div class="fabric">
        {fabric}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # CARE INSTRUCTIONS
    # ========================================================

    st.markdown(
        """
        <div class="section">

        <div class="section-title">
        Care Instructions
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="card washing">
        <b>Washing</b><br>
        {washing}
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="card bleaching">
        <b>Bleaching</b><br>
        {bleaching}
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="card drying">
        <b>Drying</b><br>
        {drying}
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="card ironing">
        <b>Ironing</b><br>
        {ironing}
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="card cleaning">
        <b>Dry Cleaning</b><br>
        {cleaning}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # SPECIAL INSTRUCTIONS
    # ========================================================

    if special:

        st.markdown(
            """
            <div class="section">

            <div class="section-title">
            Special Instructions
            </div>
            """,
            unsafe_allow_html=True
        )

        for instruction in special:

            st.markdown(
                f"""
                <div class="symbol">
                {instruction}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # ========================================================
    # CARE SYMBOLS
    # ========================================================

    symbols = detect_symbols(
        image,
        text
    )

    st.markdown(
        """
        <div class="section">

        <div class="section-title">
        Care Symbol Detection
        </div>
        """,
        unsafe_allow_html=True
    )

    if symbols:

        for symbol in symbols:

            st.markdown(
                f"""
                <div class="symbol">
                {symbol}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            """
            <div class="symbol">
            No care symbols detected.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # ALERTS
    # ========================================================

    st.markdown(
        """
        <div class="section">

        <div class="section-title">
        Important Care Alerts
        </div>
        """,
        unsafe_allow_html=True
    )

    if alerts:

        for alert in alerts:

            st.markdown(
                f"""
                <div class="alert">
                {alert}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            """
            <div class="alert">
            Follow all care instructions shown on the label.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # FINAL CARE REPORT
    # ========================================================

    special_html = ""

    if special:

        for item in special:

            special_html += (
                f"<li>{item}</li>"
            )

    else:

        special_html = (
            "<li>"
            "No additional special instructions detected."
            "</li>"
        )


    alerts_html = ""

    if alerts:

        for alert in alerts:

            alerts_html += (
                f"<li>{alert}</li>"
            )

    else:

        alerts_html = (
            "<li>"
            "Follow all care instructions shown on the label."
            "</li>"
        )


    st.markdown(
        """
        <div class="section">

        <div class="section-title">
        Final Care Report
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="report">

        <div class="report-heading">
        Fabric Information
        </div>

        {fabric}

        <div class="report-heading">
        Washing
        </div>

        {washing}

        <div class="report-heading">
        Bleaching
        </div>

        {bleaching}

        <div class="report-heading">
        Drying
        </div>

        {drying}

        <div class="report-heading">
        Ironing
        </div>

        {ironing}

        <div class="report-heading">
        Dry Cleaning
        </div>

        {cleaning}

        <div class="report-heading">
        Special Instructions
        </div>

        <ul>
        {special_html}
        </ul>

        <div class="report-heading">
        Important Care Alerts
        </div>

        <ul>
        {alerts_html}
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # DOWNLOAD REPORT
    # ========================================================

    report_text = f"""
AI-POWERED CLOTHING CARE LABEL ASSISTANT

FABRIC INFORMATION
{fabric}

WASHING
{washing}

BLEACHING
{bleaching}

DRYING
{drying}

IRONING
{ironing}

DRY CLEANING
{cleaning}

SPECIAL INSTRUCTIONS
"""

    if special:

        for item in special:

            report_text += (
                f"- {item}\n"
            )

    else:

        report_text += (
            "- No additional special instructions detected.\n"
        )


    report_text += """

IMPORTANT CARE ALERTS
"""

    for alert in alerts:

        report_text += (
            f"- {alert}\n"
        )


    st.download_button(
        "Download Care Report",
        report_text,
        file_name="clothing_care_report.txt",
        mime="text/plain"
    )
