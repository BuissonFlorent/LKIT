import sys
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow
from storage import StorageManager
from models import Person, Conversation
from datetime import date

def test_storage():
    """Test basic storage operations"""
    storage = StorageManager()
    
    # Test 1: Saving and loading a person with initial conversation
    person = Person(
        first_name="John",
        last_name="Doe",
        email="john@example.com"
    )
    conversation = Conversation(
        date=date.today(),
        notes="First meeting"
    )
    storage.save_person(person, [conversation])
    
    # Test loading the person back
    result = storage.load_person(person.id)
    if result is None:
        print("Error: Failed to load saved person")
        return
    
    loaded_person, loaded_conversations = result
    
    # Verify initial data
    assert loaded_person.first_name == person.first_name, "First name mismatch"
    assert loaded_person.last_name == person.last_name, "Last name mismatch"
    assert loaded_person.email == person.email, "Email mismatch"
    assert len(loaded_conversations) == 1, "Conversation count mismatch"
    assert loaded_conversations[0].notes == conversation.notes, "Conversation notes mismatch"
    
    # Test 2: Adding a new conversation
    new_conversation = Conversation(
        date=date.today(),
        notes="Follow-up meeting"
    )
    success = storage.add_conversation(person.id, new_conversation)
    assert success, "Failed to add new conversation"
    
    # Verify the new conversation was added
    result = storage.load_person(person.id)
    if result is None:
        print("Error: Failed to load person after adding conversation")
        return
    
    loaded_person, loaded_conversations = result
    assert len(loaded_conversations) == 2, "New conversation not added"
    assert any(c.notes == "Follow-up meeting" for c in loaded_conversations), "New conversation notes not found"
    assert all(c.person_id == person.id for c in loaded_conversations), "Conversation person_id mismatch"
    assert len({c.id for c in loaded_conversations}) == 2, "Conversation IDs not unique"
    
    print("All storage tests passed successfully!")

def main():
    app = QApplication(sys.argv)
    
    # Run storage tests
    test_storage()
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()