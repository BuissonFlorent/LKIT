import unittest
import tempfile
import shutil
from pathlib import Path
from storage import StorageManager
from models import Person, Conversation
from datetime import date

class TestStorage(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory for test data"""
        self.temp_dir = Path(tempfile.mkdtemp())
        # Override the storage base directory for testing
        self.storage = StorageManager()
        self.storage.base_dir = self.temp_dir
        self.storage.persons_dir = self.temp_dir / 'persons'
        self.storage.ensure_directories()
    
    def tearDown(self):
        """Clean up the temporary directory after tests"""
        shutil.rmtree(self.temp_dir)
    
    def test_save_and_load_person(self):
        """Test saving and loading a person with initial conversation"""
        # Create test data
        person = Person(
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )
        conversation = Conversation(
            date=date.today(),
            notes="First meeting"
        )
        
        # Test saving
        self.storage.save_person(person, [conversation])
        
        # Test loading
        result = self.storage.load_person(person.id)
        self.assertIsNotNone(result, "Failed to load saved person")
        
        loaded_person, loaded_conversations = result
        
        # Verify person data
        self.assertEqual(loaded_person.first_name, person.first_name)
        self.assertEqual(loaded_person.last_name, person.last_name)
        self.assertEqual(loaded_person.email, person.email)
        
        # Verify conversation data
        self.assertEqual(len(loaded_conversations), 1)
        self.assertEqual(loaded_conversations[0].notes, conversation.notes)
    
    def test_add_conversation(self):
        """Test adding a new conversation to existing person"""
        # Create and save initial person with conversation
        person = Person(
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )
        conversation = Conversation(
            date=date.today(),
            notes="First meeting"
        )
        self.storage.save_person(person, [conversation])
        
        # Add new conversation
        new_conversation = Conversation(
            date=date.today(),
            notes="Follow-up meeting"
        )
        success = self.storage.add_conversation(person.id, new_conversation)
        self.assertTrue(success, "Failed to add new conversation")
        
        # Verify the new conversation was added
        result = self.storage.load_person(person.id)
        self.assertIsNotNone(result, "Failed to load person after adding conversation")
        
        loaded_person, loaded_conversations = result
        self.assertEqual(len(loaded_conversations), 2, "New conversation not added")
        self.assertTrue(
            any(c.notes == "Follow-up meeting" for c in loaded_conversations),
            "New conversation notes not found"
        )
        self.assertTrue(
            all(c.person_id == person.id for c in loaded_conversations),
            "Conversation person_id mismatch"
        )
        self.assertEqual(
            len({c.id for c in loaded_conversations}), 2,
            "Conversation IDs not unique"
        )

if __name__ == '__main__':
    unittest.main() 