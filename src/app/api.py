from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import io, fitz

from .preprocess import preprocess_image
from .ocr import run_ocr
from .extractor import extract_fields

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/ui/static"), name="static")
templates = Jinja2Templates(directory="src/ui/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def pdf_to_image(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc.load_page(0)
    pix = page.get_pixmap()
    return Image.open(io.BytesIO(pix.tobytes("png")))


@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    try:
        content = await file.read()

        # Handle PDF or Image
        if file.filename.lower().endswith(".pdf"):
            img = pdf_to_image(content)
        else:
            img = Image.open(io.BytesIO(content)).convert("RGB")

        img = preprocess_image(img)

        # OCR
        text = run_ocr(img)

        # Field Extraction
        fields = extract_fields(text)

        return {
            "success": True,
            "fields": fields   # ✅ ONLY structured fields returned
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
