# AI-Powered Clothing Care Label Assistant

An OCR-based Streamlit application that extracts clothing care label information from images and provides easy-to-understand care instructions.

## Features

- Upload clothing care label images
- Extract text using Tesseract OCR
- Detect fabric composition
- Detect clothing care symbols
- Analyze washing instructions
- Analyze bleaching instructions
- Analyze drying instructions
- Analyze ironing instructions
- Analyze dry-cleaning instructions
- Generate important care alerts
- Generate a final clothing care report
- Download the care report

## Technologies Used

- Python
- Streamlit
- Tesseract OCR
- Pytesseract
- OpenCV
- NumPy
- Pillow

## Project Structure

```text
Clothing-Care-AI/
│
├── app.py
├── ocr.py
├── symbol_detection.py
├── requirements.txt
├── packages.txt
└── README.md
```

## How It Works
```text
**Upload Image**  
↓  
**OCR Text Extraction**  
↓  
**Text Cleaning**  
↓  
**Fabric Detection**  
↓  
**Care Symbol Detection**  
↓  
**Care Instruction Analysis**  
↓  
**Care Alerts**  
↓  
**Final Care Report**
```
Installation

Install the required Python packages:

```text
pip install -r requirements.tx
```
Make sure Tesseract OCR is installed on the system.

Run the Application

```text
streamlit run app.py
```
The application will open in the browser.

Example

The application can identify information such as:

```text
98% Cotton
2% Elastane

Machine Wash Cold
Do Not Bleach
Tumble Dry Low
Iron Low
Dry Clean
```
It then converts these instructions into simple clothing-care recommendations.

Deployment

This project can be deployed using Streamlit Community Cloud.
