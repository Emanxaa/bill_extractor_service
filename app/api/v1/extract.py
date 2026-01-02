from fastapi import UploadFile, File
from app.pipelines.extraction import run_extraction
from fastapi import APIRouter
router = APIRouter()

@router.post("/extract")
async def extract_financial(file: UploadFile = File(...)):
    file_bytes = await file.read()
    return run_extraction(file_bytes, file.content_type)
