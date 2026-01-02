from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class Note(BaseModel):
    raw: Optional[str] = None
    clean: Optional[str] = None

class Party(BaseModel):
    name: Optional[str] = None
    account_number: Optional[str] = None


class FinancialExtraction(BaseModel):
    transaction_datetime: Optional[datetime]
    transaction_amount: Optional[float]
    currency: Optional[str]
    transaction_type: Optional[str]
    platform: Optional[str]
    reference_number: Optional[str]

    note: Optional[Note]

    source: dict | None
    destination: dict | None
