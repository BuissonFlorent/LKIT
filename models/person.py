from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Person:
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    birth_date: Optional[date] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = ""
    
    @property
    def full_name(self) -> str:
        """Returns the full name of the person."""
        return " ".join(filter(None, [self.first_name, self.last_name]))