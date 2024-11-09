import os
import json
from pathlib import Path
from typing import Optional, Dict, List
from datetime import date
from models import Person, Conversation

class StorageManager:
    def __init__(self):
        self.base_dir = Path.home() / '.lkit'
        self.persons_dir = self.base_dir / 'persons'
        self.ensure_directories()
        self._next_id = self._get_next_id()
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        self.persons_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_file_name(self, person: Person) -> str:
        """Generate file name in format: LastNameFirstNameID.json"""
        # Remove spaces and special characters from names
        last_name = ''.join(c for c in person.last_name if c.isalnum())
        first_name = ''.join(c for c in person.first_name if c.isalnum())
        return f"{last_name}{first_name}{person.id}.json"
    
    def _get_id_from_file_name(self, file_name: str) -> int:
        """Extract ID from file name"""
        name_without_extension = file_name.replace('.json', '')
        digits = ''
        for char in reversed(name_without_extension):
            if char.isdigit():
                digits = char + digits
            else:
                break
        return int(digits) if digits else 0
    
    def _get_next_id(self) -> int:
        """Find the next available ID by checking existing files"""
        existing_ids = [
            self._get_id_from_file_name(f.name)
            for f in self.persons_dir.glob('*.json')
        ]
        return max(existing_ids, default=0) + 1
    
    def _person_to_dict(self, person: Person, conversations: List[Conversation]) -> Dict:
        """Convert person and conversations to a dictionary for JSON storage"""
        return {
            "id": person.id,
            "first_name": person.first_name,
            "last_name": person.last_name,
            "email": person.email,
            "phone": person.phone,
            "birth_date": person.birth_date.isoformat() if person.birth_date else None,
            "notes": person.notes,
            "conversations": [
                {
                    "id": conv.id,
                    "date": conv.date.isoformat(),
                    "notes": conv.notes
                }
                for conv in conversations
            ]
        }
    
    def _dict_to_person(self, data: Dict) -> tuple[Person, List[Conversation]]:
        """Convert dictionary data back to Person and Conversation objects"""
        # Convert birth_date string back to date object if it exists
        birth_date = None
        if data.get('birth_date'):
            birth_date = date.fromisoformat(data['birth_date'])
        
        person = Person(
            id=data['id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data.get('email'),
            phone=data.get('phone'),
            birth_date=birth_date,
            notes=data.get('notes')
        )
        
        conversations = []
        for conv_data in data.get('conversations', []):
            conversation = Conversation(
                id=conv_data['id'],
                person_id=person.id,
                date=date.fromisoformat(conv_data['date']),
                notes=conv_data['notes']
            )
            conversations.append(conversation)
        
        return person, conversations
    
    def save_person(self, person: Person, conversations: List[Conversation]) -> None:
        """Save person and their conversations to a JSON file"""
        if person.id is None:
            person.id = self._next_id
            self._next_id += 1
        
        # Ensure conversations have IDs and person_id
        for i, conv in enumerate(conversations):
            if conv.id is None:
                conv.id = i + 1
            conv.person_id = person.id
        
        data = self._person_to_dict(person, conversations)
        file_path = self.persons_dir / self._get_file_name(person)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_person(self, person_id: int) -> Optional[tuple[Person, List[Conversation]]]:
        """Load person and their conversations from JSON file"""
        try:
            for file_path in self.persons_dir.glob('*.json'):
                file_id = self._get_id_from_file_name(file_path.name)
                if file_id == person_id:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        return self._dict_to_person(data)
            return None
        except Exception as e:
            print(f"Error loading person {person_id}: {str(e)}")
            return None
    
    def get_all_persons(self) -> List[Person]:
        """Load all persons (without conversations) for listing"""
        persons = []
        for file_path in self.persons_dir.glob('*.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                person, _ = self._dict_to_person(data)
                persons.append(person)
        return persons
    
    @property
    def is_initialized(self) -> bool:
        """Check if the storage structure is properly initialized"""
        return self.persons_dir.exists() 