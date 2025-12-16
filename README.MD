# Document Extractor – PAN / Aadhaar / GST / Bank

## Project Overview
This project is an automated document extraction system developed using Python and OCR.
It extracts structured information from scanned documents such as PAN cards, Aadhaar cards,
GST certificates, and Bank passbooks, and presents the extracted data in a structured format
suitable for ERP vendor master integration.

The system uses Optical Character Recognition (OCR) combined with rule-based extraction
techniques to identify and extract relevant fields with confidence scores.

---

## Supported Documents & Extracted Fields

| Document Type | Extracted Fields |
|--------------|------------------|
| PAN Card | PAN Number, Name, Father Name, Date of Birth |
| Aadhaar Card | Aadhaar Number, Name, Address |
| GST Certificate | GSTIN, Business Name, Address, Registration Type |
| Bank Passbook | Bank Name, Account Number, IFSC Code, Account Holder Name |

---

## Technologies Used
- Python 3.10+
- FastAPI (Backend REST API)
- Tesseract OCR
- OpenCV (Image preprocessing)
- PyMuPDF (PDF handling)
- HTML, CSS, JavaScript (Frontend UI)
- pytest (Unit testing)

---

## Environment Setup

## 1. Install Tesseract OCR
- Download and install Tesseract OCR
- Add Tesseract installation directory to system PATH

## 2. Create Virtual Environment
```bash
python -m venv venv

## Activate the Virtual Environment

Windows:
```bash
venv\Scripts\activate



Linux / macOS
```bash
source venv/bin/activate

## 3. Install Project Dependencies
pip install -r requirements.txt

## Running the Application
Start the FastAPI Server
```bash
uvicorn src.app.api:app --reload

## Open the Application in Browser
```bash
http://127.0.0.1:8000

## How It Works
- The user uploads an image or PDF document through the web interface.
- The document is preprocessed to improve OCR accuracy.
- OCR is applied to extract raw text from the document.
- Rule-based and pattern-based logic extracts the required fields.
- Each extracted field is assigned a confidence score.
- The extracted results are displayed in a professional web interface.

**Sample Data**
Sample documents used for testing and demonstration are available in:

data/samples/


**Output Format**
- Extracted fields displayed in a structured table format
- Confidence score provided for each extracted field
- Graceful handling of unreadable or low-quality documents

**Unit Testing**
Basic unit tests are implemented using pytest to validate core extraction logic.

Run tests using:
```bash
pytest

**Limitations**
- OCR accuracy depends on document image quality
- Handwritten documents are not supported
- Multi-page PDF processing is limited to the first page

**Future Enhancements**
- Multi-page PDF support
- ERP system integration via APIs
- Government verification APIs (GST / Aadhaar validation)
- Machine learning-based entity extraction



