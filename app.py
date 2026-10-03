import streamlit as st
import re

from PIL import Image

from ocr import extract_text
from symbol_detection import detect_symbols


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI-Powered Clothing Care Label Assistant",
    layout="centered"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("AI-Powered Clothing Care Label Assistant")

st.write(
    "Upload a clothing care label image to extract and "
    "understand its care instructions using OCR."
)


# --------------------------------------------------
# IMAGE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Clothing Care Label",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file:

    # --------------------------------------------------
    # LOAD IMAGE
    # --------------------------------------------------

    image = Image.open(uploaded_file)

    st.subheader("Uploaded Image")

    st.image(
        image,
        use_container_width=True
    )


    # --------------------------------------------------
    # OCR
    # --------------------------------------------------

    text = extract_text(image)


    # --------------------------------------------------
    # OCR RESULT
    # --------------------------------------------------

    st.subheader("OCR Result")

    if text:

        st.text_area(
            "Extracted Text",
            text,
            height=180
        )

        care_text = text.upper()


        # --------------------------------------------------
        # FABRIC INFORMATION
        # --------------------------------------------------

        st.subheader("Fabric Information")

        fabric_parts = []

        fabric_patterns = {
            "Cotton": r"(\d+)\s*%\s*COTTON",
            "Elastane": r"(\d+)\s*%\s*ELASTANE",
            "Polyester": r"(\d+)\s*%\s*POLYESTER",
            "Nylon": r"(\d+)\s*%\s*NYLON",
            "Wool": r"(\d+)\s*%\s*WOOL",
            "Viscose": r"(\d+)\s*%\s*VISCOSE",
            "Linen": r"(\d+)\s*%\s*LINEN",
            "Silk": r"(\d+)\s*%\s*SILK"
        }

        for fabric, pattern in fabric_patterns.items():

            match = re.search(
                pattern,
                care_text
            )

            if match:

                fabric_parts.append(
                    f"{match.group(1)}% {fabric}"
                )


        if fabric_parts:

            st.success(
                "Fabric: "
                + " + ".join(fabric_parts)
            )

        else:

            st.info(
                "Fabric composition was not detected."
            )


        # --------------------------------------------------
        # CARE SYMBOL DETECTION
        # --------------------------------------------------

        st.subheader("Care Symbol Detection")

        symbols = detect_symbols(
            image,
            text
        )

        if symbols:

            for symbol in symbols:

                st.write(
                    symbol
                )

        else:

            st.info(
                "No care symbols were detected."
            )


        # --------------------------------------------------
        # CARE VARIABLES
        # --------------------------------------------------

        washing = "Not detected"
        bleaching = "Not detected"
        drying = "Not detected"
        ironing = "Not detected"
        dry_cleaning = "Not detected"


        # --------------------------------------------------
        # WASHING
        # --------------------------------------------------

        if "MACHINE WASH COLD" in care_text:

            washing = "Machine wash with cold water"

        elif "HAND WASH COLD" in care_text:

            washing = "Hand wash using cold water"

        elif "WASH COLD" in care_text:

            washing = "Wash using cold water"

        elif "MACHINE WASH WARM" in care_text:

            washing = "Machine wash with warm water"

        elif "WASH WARM" in care_text:

            washing = "Wash using warm water"

        elif "MACHINE WASH HOT" in care_text:

            washing = "Machine wash with hot water"

        elif "WASH HOT" in care_text:

            washing = "Wash using hot water"

        elif "MACHINE WASH" in care_text:

            washing = "Machine wash"

        elif "HAND WASH" in care_text:

            washing = "Hand wash"

        elif "WASH" in care_text:

            washing = "Follow the washing instructions"


        # --------------------------------------------------
        # BLEACH
        # --------------------------------------------------

        if "DO NOT BLEACH" in care_text:

            bleaching = "Do not use bleach"

        elif "NO BLEACH" in care_text:

            bleaching = "Do not use bleach"

        elif "BLEACH" in care_text:

            bleaching = "Bleach instruction detected"


        # --------------------------------------------------
        # DRYING
        # --------------------------------------------------

        if "DO NOT TUMBLE DRY" in care_text:

            drying = "Do not tumble dry"

        elif "TUMBLE DRY LOW" in care_text:

            drying = "Tumble dry using low heat"

        elif "TUMBLE DRY MEDIUM" in care_text:

            drying = "Tumble dry using medium heat"

        elif "TUMBLE DRY HIGH" in care_text:

            drying = "Tumble dry using high heat"

        elif "TUMBLE DRY" in care_text:

            drying = "Tumble drying is allowed"

        elif "DRY FLAT" in care_text:

            drying = "Dry flat"

        elif "LINE DRY" in care_text:

            drying = "Line dry"

        elif "AIR DRY" in care_text:

            drying = "Air dry"


        # --------------------------------------------------
        # IRONING
        # --------------------------------------------------

        if "DO NOT IRON" in care_text:

            ironing = "Do not iron"

        elif "IRON LOW" in care_text:

            ironing = "Iron at low temperature"

        elif "LOW IRON" in care_text:

            ironing = "Iron at low temperature"

        elif "IRON MEDIUM" in care_text:

            ironing = "Iron at medium temperature"

        elif "MEDIUM IRON" in care_text:

            ironing = "Iron at medium temperature"

        elif "IRON HIGH" in care_text:

            ironing = "Iron at high temperature"

        elif "HIGH IRON" in care_text:

            ironing = "Iron at high temperature"

        elif "IRON" in care_text:

            ironing = "Follow the ironing instructions"


        # --------------------------------------------------
        # DRY CLEANING
        # --------------------------------------------------

        if "DO NOT DRY CLEAN" in care_text:

            dry_cleaning = "Do not dry clean"

        elif "DRY CLEAN" in care_text:

            dry_cleaning = "Dry cleaning is allowed"


        # --------------------------------------------------
        # CLOTHING CARE ANALYSIS
        # --------------------------------------------------

        st.subheader("Clothing Care Analysis")

        st.write(
            "Washing: " + washing
        )

        st.write(
            "Bleach: " + bleaching
        )

        st.write(
            "Drying: " + drying
        )

        st.write(
            "Ironing: " + ironing
        )

        st.write(
            "Dry Cleaning: " + dry_cleaning
        )


        # --------------------------------------------------
        # IMPORTANT CARE ALERTS
        # --------------------------------------------------

        alerts = []


        if "DO NOT BLEACH" in care_text:

            alerts.append(
                "Avoid using bleach."
            )


        if "TUMBLE DRY LOW" in care_text:

            alerts.append(
                "Use low heat while tumble drying."
            )


        if "TUMBLE DRY HIGH" in care_text:

            alerts.append(
                "High heat is mentioned for drying."
            )


        if "DO NOT TUMBLE DRY" in care_text:

            alerts.append(
                "Do not tumble dry this clothing."
            )


        if "IRON LOW" in care_text:

            alerts.append(
                "Use low temperature while ironing."
            )


        if "DO NOT IRON" in care_text:

            alerts.append(
                "Do not iron this clothing."
            )


        if "DO NOT DRY CLEAN" in care_text:

            alerts.append(
                "Do not dry clean this clothing."
            )


        if alerts:

            st.subheader("Important Care Alerts")

            for alert in alerts:

                st.warning(
                    alert
                )


        # --------------------------------------------------
        # FINAL REPORT
        # --------------------------------------------------

        st.subheader(
            "Final Clothing Care Report"
        )

        st.markdown("---")


        if fabric_parts:

            st.write(
                "Fabric: "
                + " + ".join(fabric_parts)
            )

        else:

            st.write(
                "Fabric: Not detected"
            )


        st.write(
            "Washing: " + washing
        )

        st.write(
            "Bleach: " + bleaching
        )

        st.write(
            "Drying: " + drying
        )

        st.write(
            "Ironing: " + ironing
        )

        st.write(
            "Dry Cleaning: " + dry_cleaning
        )


        st.markdown("---")


        # --------------------------------------------------
        # EASY-TO-UNDERSTAND INSTRUCTIONS
        # --------------------------------------------------

        st.subheader(
            "Easy-to-Understand Instructions"
        )


        summary = []


        if washing != "Not detected":

            summary.append(
                "Wash: " + washing
            )


        if bleaching != "Not detected":

            summary.append(
                "Bleach: " + bleaching
            )


        if drying != "Not detected":

            summary.append(
                "Dry: " + drying
            )


        if ironing != "Not detected":

            summary.append(
                "Iron: " + ironing
            )


        if dry_cleaning != "Not detected":

            summary.append(
                "Dry Cleaning: " + dry_cleaning
            )


        if summary:

            for item in summary:

                st.write(
                    "- " + item
                )

        else:

            st.write(
                "No specific care instructions were identified."
            )


        # --------------------------------------------------
        # DOWNLOAD REPORT
        # --------------------------------------------------

        report = f"""
AI-Powered Clothing Care Label Assistant
========================================

OCR Extracted Text
------------------
{text}

Fabric Information
------------------
{", ".join(fabric_parts) if fabric_parts else "Not detected"}

Care Symbols
------------
{", ".join(symbols) if symbols else "Not detected"}

Clothing Care Analysis
----------------------
Washing: {washing}
Bleach: {bleaching}
Drying: {drying}
Ironing: {ironing}
Dry Cleaning: {dry_cleaning}

Important Care Alerts
---------------------
{chr(10).join(alerts) if alerts else "No important alerts detected."}

Easy-to-Understand Instructions
--------------------------------
{chr(10).join(summary) if summary else "No specific care instructions were identified."}
"""


        st.subheader("Download Report")


        st.download_button(
            label="Download Care Report",
            data=report,
            file_name="clothing_care_report.txt",
            mime="text/plain"
        )


    else:

        st.warning(
            "No text detected. Please upload a clearer clothing label image."
        )