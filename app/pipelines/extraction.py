from app.services.ocr_service import extract_text_from_bytes
from app.services.llm_service import extract_financial_with_llm
from app.pipelines.mapper import map_llm_to_schema


def run_extraction(file_bytes: bytes, mime_type: str):
    # 1. OCR
    ocr_text = extract_text_from_bytes(file_bytes, mime_type)

    # (DEV ONLY) log OCR
    print("=== OCR TEXT START ===")
    print(ocr_text)
    print("=== OCR TEXT END ===")

    # 2. LLM extraction  ← ← ← INI YANG SEBELUMNYA TIDAK ADA
    llm_data = extract_financial_with_llm(ocr_text)

    # (DEV ONLY) log LLM output
    print("=== LLM JSON START ===")
    print(llm_data)
    print("=== LLM JSON END ===")

    # 3. Map to schema (Pydantic validation)
    result = map_llm_to_schema(
        llm_data,
        document_type=mime_type,
    )

    return result
