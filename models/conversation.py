from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Conversation:
    id: Optional[int] = None
    person_id: Optional[int] = None
    date: date = date.today()
    notes: str = "" 