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

.stApp {
    background-color: #0b0d12;
    color: #ffffff;
}

.main {
    background-color: #0b0d12;
}

h1, h2, h3, h4, p, label {
    color: #ffffff !important;
}

.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    color: #ffffff !important;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #c7c7c7 !important;
    font-size: 17px;
    margin-bottom: 30px;
}


/* Common Card */

.box {
    padding: 18px;
    border-radius: 15px;
    margin: 12px 0;
    color: #ffffff !important;
    font-size: 16px;
    background-color: #151821;
    box-shadow: 0 3px 12px rgba(0,0,0,0.35);
}

.box b {
    color: #ffffff !important;
}


/* Fabric */

.fabric {
    background: #211936;
    border-left: 7px solid #a855f7;
}


/* Washing */

.wash {
    background: #10243b;
    border-left: 7px solid #2196f3;
}


/* Bleaching */

.bleach {
    background: #35151b;
    border-left: 7px solid #ff3b4d;
}


/* Drying */

.dry {
    background: #38240f;
    border-left: 7px solid #ff9800;
}


/* Ironing */

.iron {
    background: #103329;
    border-left: 7px solid #20d9a0;
}


/* Dry Cleaning */

.clean {
    background: #302018;
    border-left: 7px solid #b77961;
}


/* Symbols */

.symbol {
    background: #26142e;
    border-left: 7px solid #c026d3;
}


/* Alerts */

.alert {
    background: #35151b;
    border-left: 7px solid #ff304f;
}


/* Report */

.report {
    background: #151d35;
    border-left: 7px solid #4f7cff;
}


/* Text Area */

textarea {
    background-color: #151821 !important;
    color: #ffffff !important;
    border: 1px solid #555 !important;
}


/* File uploader */

[data-testid="stFileUploader"] {
    background-color: #151821;
    border-radius: 12px;
    padding: 10px;
}


/* Buttons */

.stDownloadButton button {
    background-color: #6d28d9;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
}

.stDownloadButton button:hover {
    background-color: #8b5cf6;
}


/* Success message */

[data-testid="stAlert"] {
    color: white !important;
}


/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #101218;
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

</style>
""", unsafe_allow_html=True)


st.markdown(
    '<div class="main-title">'
    'AI-Powered Clothing Care Label Assistant'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'OCR-based clothing care label analysis and recommendation system'
    '</div>',
    unsafe_allow_html=True
)


with st.sidebar:

    st.header("Project Information")

    st.write(
        "Upload a clothing care label image. "
        "The system extracts fabric information "
        "and clothing care instructions."
    )

    st.divider()

    st.subheader("Technologies")

    st.write("Python")
    st.write("Streamlit")
    st.write("Tesseract OCR")
    st.write("OpenCV")
    st.write("NumPy")
    st.write("Pillow")



st.header("Upload Clothing Care Label")

uploaded_file = st.file_uploader(
    "Choose a clothing care label image",
    type=["jpg", "jpeg", "png", "webp"]
)


if uploaded_file:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Clothing Label",
        width="stretch"
    )



    with st.spinner("Analyzing clothing label..."):

        raw_text = extract_text(image)


    def clean_display_text(text):

        text = text.upper()

        result = []

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

        if "DO NOT BLEACH" in text:

            result.append("DO NOT BLEACH")

        elif "NO BLEACH" in text:

            result.append("NO BLEACH")

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

        if "DO NOT IRON" in text:

            result.append("DO NOT IRON")

        elif "IRON LOW" in text:

            result.append("IRON LOW")

        elif "IRON MEDIUM" in text:

            result.append("IRON MEDIUM")

        elif "IRON HIGH" in text:

            result.append("IRON HIGH")

        if "DO NOT DRY CLEAN" in text:

            result.append("DO NOT DRY CLEAN")

        elif "DRY CLEAN" in text:

            result.append("DRY CLEAN")

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

        final = []

        for item in result:

            if item not in final:

                final.append(item)

        return "\n".join(final)


    text = clean_display_text(raw_text)

    upper = text.upper()


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
            + '</div>',
            unsafe_allow_html=True
        )

    else:

        st.info("Fabric composition not detected.")

    st.header("Care Instructions")

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

    if "DO NOT BLEACH" in upper:

        bleaching = "Do not use bleach"

    elif "NO BLEACH" in upper:

        bleaching = "Do not use bleach"

    else:

        bleaching = "Not detected"

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


    if "DO NOT DRY CLEAN" in upper:

        cleaning = "Do not dry clean"

    elif "DRY CLEAN" in upper:

        cleaning = "Dry cleaning is allowed"

    else:

        cleaning = "Not detected"


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
        '<div class="box report">'
        '<b>Care Report</b><br><br>'
        '<pre style="color:white; background:transparent;">'
        + report +
        '</pre>'
        '</div>',
        unsafe_allow_html=True
    )




    st.download_button(
        "Download Care Report",
        report,
        file_name="clothing_care_report.txt",
        mime="text/plain"
    )
