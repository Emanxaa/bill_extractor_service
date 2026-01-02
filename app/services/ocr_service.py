from io import BytesIO
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes

def extract_text_from_bytes(
    file_bytes: bytes,
    content_type: str
) -> str:
    if content_type == "application/pdf":
        pages = convert_from_bytes(file_bytes)
        return "\n".join(pytesseract.image_to_string(p) for p in pages)

    image = Image.open(BytesIO(file_bytes))
    return pytesseract.image_to_string(image)
