from dataclasses import dataclass, field
from datetime import date
from typing import Optional

@dataclass
class Conversation:
    id: Optional[int] = None
    person_id: Optional[int] = None
    date: date = field(default_factory=date.today) # type: ignore
    notes: str = "" 