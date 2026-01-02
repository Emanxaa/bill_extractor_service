import json
from typing import Dict

from google import genai
from google.genai import types

from app.core.config import settings


class LLMExtractionError(Exception):
    pass


if not settings.GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")


def _build_prompt(ocr_text: str) -> str:
    return f"""
You are an information extraction engine.

INSTRUCTIONS:
- Extract values ONLY from the text below.
- Capture any memo, remark, note, or free-text description under note.raw
- If multiple notes exist, concatenate them with a single space
- If no notes exist, set note.raw to null
- Fill ONLY the fields defined in the schema.
- If a value is missing or unclear, return null.
- Do NOT guess.
- Do NOT explain.
- Do NOT add extra fields.
- Return VALID JSON only.

TEXT:
\"\"\"
{ocr_text}
\"\"\"

SCHEMA:
{{
  "transaction_datetime": "string | null",
  "transaction_amount": "number | null",
  "currency": "string | null",
  "transaction_type": "string | null",
  "platform": "string | null",
  "reference_number": "string | null",
  "source": {{
    "name": "string | null",
    "account_number": "string | null"
  }},
  "destination": {{
    "name": "string | null",
    "account_number": "string | null"
  }}
}}
""".strip()


def extract_financial_with_llm(ocr_text: str) -> Dict:
    if not ocr_text.strip():
        raise LLMExtractionError("Empty OCR text")

    prompt = _build_prompt(ocr_text)

    try:
        client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,
                top_p=0.1,
                response_mime_type="application/json",
            ),
        )

    except Exception as e:
        raise LLMExtractionError(f"Gemini request failed: {e}")

    try:
        raw_text = response.text.strip()
        return json.loads(raw_text)
    except Exception as e:
        raise LLMExtractionError(f"Invalid Gemini response: {e}")
