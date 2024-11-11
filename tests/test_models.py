import unittest
from datetime import date
from models import Person, Conversation

class TestPerson(unittest.TestCase):
    def test_person_creation(self):
        """Test creating a person with various fields"""
        person = Person(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="123-456-7890",
            birth_date=date(1990, 1, 1),
            notes="Test notes"
        )
        
        self.assertEqual(person.first_name, "John")
        self.assertEqual(person.last_name, "Doe")
        self.assertEqual(person.email, "john@example.com")
        self.assertEqual(person.phone, "123-456-7890")
        self.assertEqual(person.birth_date, date(1990, 1, 1))
        self.assertEqual(person.notes, "Test notes")
    
    def test_person_optional_fields(self):
        """Test creating a person with only required fields"""
        person = Person(
            first_name="John",
            last_name="Doe"
        )
        
        self.assertEqual(person.first_name, "John")
        self.assertEqual(person.last_name, "Doe")
        self.assertIsNone(person.email)
        self.assertIsNone(person.phone)
        self.assertIsNone(person.birth_date)
        self.assertEqual(person.notes, "")
    
    def test_full_name(self):
        """Test the full_name property"""
        person = Person(first_name="John", last_name="Doe")
        self.assertEqual(person.full_name, "John Doe")
        
        # Test with empty last name
        person = Person(first_name="John", last_name="")
        self.assertEqual(person.full_name, "John")
        
        # Test with empty first name
        person = Person(first_name="", last_name="Doe")
        self.assertEqual(person.full_name, "Doe")

class TestConversation(unittest.TestCase):
    def test_conversation_creation(self):
        """Test creating a conversation with all fields"""
        conv = Conversation(
            id=1,
            person_id=2,
            date=date(2024, 1, 1),
            notes="Test conversation"
        )
        
        self.assertEqual(conv.id, 1)
        self.assertEqual(conv.person_id, 2)
        self.assertEqual(conv.date, date(2024, 1, 1))
        self.assertEqual(conv.notes, "Test conversation")
    
    def test_conversation_defaults(self):
        """Test creating a conversation with minimal fields"""
        today = date.today()
        conv = Conversation(notes="Test notes")
        
        self.assertIsNone(conv.id)
        self.assertIsNone(conv.person_id)
        self.assertEqual(conv.date, today)
        self.assertEqual(conv.notes, "Test notes")
    
    def test_empty_conversation(self):
        """Test creating a conversation with no fields"""
        today = date.today()
        conv = Conversation()
        
        self.assertIsNone(conv.id)
        self.assertIsNone(conv.person_id)
        self.assertEqual(conv.date, today)
        self.assertEqual(conv.notes, "")

if __name__ == '__main__':
    unittest.main() 