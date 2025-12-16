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

Activate the virtual environment:

Windows

venv\Scripts\activate


Linux / macOS

source venv/bin/activate

📦 3. Install Project Dependencies

Install required Python libraries:

pip install -r requirements.txt

🚀 4. Run the Application

Start the FastAPI server:

uvicorn src.app.api:app --reload

🌐 5. Access the Application

Open your browser and go to:

http://127.0.0.1:8000

🔍 6. How It Works

User uploads an image or PDF document

Document preprocessing is applied

OCR extracts raw text

Rule-based logic extracts required fields

Confidence scores are calculated

Results are displayed in the UI

📂 7. Sample Data

Sample documents for testing are available in:

data/samples/

📊 8. Output Format

Structured table of extracted fields

Confidence score for each field

Graceful handling of low-quality documents

🧪 9. Unit Testing

Run unit tests using pytest:

pytest

⚠️ 10. Limitations

OCR accuracy depends on image quality

Handwritten documents are not supported

Only first page of PDF is processed

🚧 11. Future Enhancements

Multi-page PDF support

ERP integration APIs

Government verification APIs

ML-based entity extraction
