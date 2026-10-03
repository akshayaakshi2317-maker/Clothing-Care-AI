import re
import streamlit as st
from PIL import Image

from ocr import extract_text
from symbol_detection import detect_symbols


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI-Powered Clothing Care Label Assistant",
    page_icon=None,
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("AI-Powered Clothing Care Label Assistant")

st.write(
    "Upload a clothing care label image to extract fabric "
    "information and care instructions using OCR."
)


# --------------------------------------------------
# FABRIC DETECTION
# --------------------------------------------------

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

    # ----------------------------------------------
    # Detect percentage + fabric
    # Example: 98% COTTON
    # ----------------------------------------------

    percentage_matches = re.findall(
        r"(\d+)\s*%\s*([A-Z]+)",
        text_upper
    )

    for percentage, fabric in percentage_matches:

        if fabric in fabric_names:

            result = f"{percentage}% {fabric.title()}"

            if result not in detected:
                detected.append(result)

    # ----------------------------------------------
    # Detect fabric names without percentage
    # ----------------------------------------------

    for fabric in fabric_names:

        if fabric in text_upper:

            # Avoid duplicate fabric name
            already_detected = False

            for item in detected:

                if fabric.title() in item:
                    already_detected = True
                    break

            if not already_detected:

                # Add only if not already included
                detected.append(fabric.title())

    # ----------------------------------------------
    # Remove duplicate plain fabric names
    # ----------------------------------------------

    final_detected = []

    for item in detected:

        if item not in final_detected:
            final_detected.append(item)

    if not final_detected:
        return "Fabric composition was not detected."

    return " + ".join(final_detected)


# --------------------------------------------------
# WASHING ANALYSIS
# --------------------------------------------------

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


# --------------------------------------------------
# BLEACH ANALYSIS
# --------------------------------------------------

def analyze_bleach(text):

    text = text.upper()

    if "DO NOT BLEACH" in text or "NO BLEACH" in text:

        return "Do not use bleach"

    if "BLEACH" in text:

        return "Check bleach instructions carefully"

    return "Bleaching instruction not detected"


# --------------------------------------------------
# DRYING ANALYSIS
# --------------------------------------------------

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


# --------------------------------------------------
# IRONING ANALYSIS
# --------------------------------------------------

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


# --------------------------------------------------
# DRY CLEANING ANALYSIS
# --------------------------------------------------

def analyze_dry_cleaning(text):

    text = text.upper()

    if "DO NOT DRY CLEAN" in text:

        return "Do not dry clean"

    if "DRY CLEAN" in text:

        return "Dry cleaning is allowed"

    return "Dry cleaning instruction not detected"


# --------------------------------------------------
# CARE ALERTS
# --------------------------------------------------

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


# --------------------------------------------------
# FINAL CARE REPORT
# --------------------------------------------------

def create_report(
    fabric,
    washing,
    bleach,
    drying,
    ironing,
    dry_cleaning
):

    report = f"""
AI-POWERED CLOTHING CARE LABEL ASSISTANT

FABRIC INFORMATION
{fabric}

WASHING
{washing}

BLEACHING
{bleach}

DRYING
{drying}

IRONING
{ironing}

DRY CLEANING
{dry_cleaning}

GENERAL RECOMMENDATION
Follow the care instructions provided on the clothing label.
"""

    return report.strip()


# --------------------------------------------------
# IMAGE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Clothing Care Label Image",
    type=["jpg", "jpeg", "png"]
)


# --------------------------------------------------
# PROCESS IMAGE
# --------------------------------------------------

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.subheader("Uploaded Image")

    st.image(
        image,
        width=500
    )

    # ----------------------------------------------
    # OCR
    # ----------------------------------------------

    with st.spinner("Extracting text from image..."):

        text = extract_text(image)

    # ----------------------------------------------
    # OCR RESULT
    # ----------------------------------------------

    st.subheader("Extracted Text")

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

    # ----------------------------------------------
    # FABRIC
    # ----------------------------------------------

    fabric = detect_fabric(text)

    st.subheader("Fabric Information")

    st.write(fabric)

    # ----------------------------------------------
    # CARE ANALYSIS
    # ----------------------------------------------

    washing = analyze_washing(text)

    bleach = analyze_bleach(text)

    drying = analyze_drying(text)

    ironing = analyze_ironing(text)

    dry_cleaning = analyze_dry_cleaning(text)

    # ----------------------------------------------
    # CARE INSTRUCTIONS
    # ----------------------------------------------

    st.subheader("Care Instructions")

    st.write("Washing:", washing)

    st.write("Bleaching:", bleach)

    st.write("Drying:", drying)

    st.write("Ironing:", ironing)

    st.write("Dry Cleaning:", dry_cleaning)

    # ----------------------------------------------
    # SYMBOL DETECTION
    # ----------------------------------------------

    st.subheader("Care Symbol Detection")

    try:

        symbols = detect_symbols(
            image,
            text
        )

        if symbols:

            for symbol in symbols:

                st.write(symbol)

        else:

            st.write(
                "No care symbols detected."
            )

    except Exception:

        st.write(
            "Care symbol detection could not be completed."
        )

    # ----------------------------------------------
    # ALERTS
    # ----------------------------------------------

    alerts = generate_alerts(
        washing,
        bleach,
        drying,
        ironing,
        dry_cleaning
    )

    st.subheader("Important Care Alerts")

    for alert in alerts:

        st.write(alert)

    # ----------------------------------------------
    # FINAL REPORT
    # ----------------------------------------------

    report = create_report(
        fabric,
        washing,
        bleach,
        drying,
        ironing,
        dry_cleaning
    )

    st.subheader("Final Care Report")

    st.text_area(
        "Report",
        report,
        height=300
    )

    # ----------------------------------------------
    # DOWNLOAD REPORT
    # ----------------------------------------------

    st.download_button(
        label="Download Care Report",
        data=report,
        file_name="clothing_care_report.txt",
        mime="text/plain"
    )