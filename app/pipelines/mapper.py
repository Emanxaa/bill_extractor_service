from datetime import datetime
from typing import Dict

from app.schemas.financial import FinancialExtraction, Party, Note
from app.utils.datetime_utils import parse_id_datetime
from app.utils.normalization_utils import (
    normalize_currency,
    normalize_platform,
    normalize_account_number,
    normalize_note,  # ← BARU
)

def map_llm_to_schema(
    llm_data: Dict,
    *,
    document_type: str,
) -> FinancialExtraction:
    """
    Map raw LLM output into FinancialExtraction schema safely.
    Acts as an anti-corruption layer between probabilistic AI output
    and deterministic system contracts.
    """

    # --- Datetime normalization ---
    raw_datetime = llm_data.get("transaction_datetime")
    parsed_datetime = (
        parse_id_datetime(raw_datetime)
        if isinstance(raw_datetime, str)
        else None
    )

    # --- Amount (defensive cast) ---
    raw_amount = llm_data.get("transaction_amount")
    try:
        amount = float(raw_amount) if raw_amount is not None else None
    except (TypeError, ValueError):
        amount = None

    # --- Parties ---
    source_raw = llm_data.get("source") or {}
    destination_raw = llm_data.get("destination") or {}

    source = (
        Party(
            name=source_raw.get("name"),
            account_number=normalize_account_number(
                source_raw.get("account_number")
            ),
        )
        if source_raw
        else None
    )

    destination = (
        Party(
            name=destination_raw.get("name"),
            account_number=normalize_account_number(
                destination_raw.get("account_number")
            ),
        )
        if destination_raw
        else None
    )

    # --- NOTE NORMALIZATION (BARU) ---
    raw_note = None
    if isinstance(llm_data.get("note"), dict):
        raw_note = llm_data["note"].get("raw")
    elif isinstance(llm_data.get("note"), str):
        raw_note = llm_data.get("note")

    normalized_note = normalize_note(raw_note)

    note = (
        Note(
            raw=normalized_note["raw"],
            clean=normalized_note["clean"],
        )
        if normalized_note["raw"]
        else None
    )

    return FinancialExtraction(
        transaction_datetime=parsed_datetime,
        transaction_amount=amount,

        currency=normalize_currency(llm_data.get("currency")),
        transaction_type=llm_data.get("transaction_type"),
        platform=normalize_platform(llm_data.get("platform")),

        reference_number=llm_data.get("reference_number"),

        note=note,  # ← BARU

        source=source.model_dump() if source else None,
        destination=destination.model_dump() if destination else None,

        uploaded_at=datetime.utcnow(),
        document_type=document_type,
        extraction_confidence=_calculate_confidence(
            parsed_datetime=parsed_datetime,
            amount=amount,
            currency=normalize_currency(llm_data.get("currency")),
            reference=llm_data.get("reference_number"),
            source=source,
            destination=destination,
            note=note,  # ← opsional
        ),
    )

def _calculate_confidence(
    *,
    parsed_datetime,
    amount,
    currency,
    reference,
    source,
    destination,
    note=None,
) -> float:
    """
    Weighted confidence scoring.
    """

    score = 0.0
    total = 0.0

    def add(value, weight):
        nonlocal score, total
        total += weight
        if value not in (None, "", []):
            score += weight

    # High importance
    add(parsed_datetime, 0.25)
    add(amount, 0.25)

    # Medium importance
    add(reference, 0.15)
    add(currency, 0.10)

    # Lower importance
    add(source.name if source else None, 0.10)
    add(destination.name if destination else None, 0.10)

    # Very low importance (note presence)
    add(note.clean if note else None, 0.05)

    return round(score / total, 2) if total > 0 else 0.0
