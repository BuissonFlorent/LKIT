import sys
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow
from storage import StorageManager
from models import Person, Conversation
from datetime import date

def test_storage():
    """Test basic storage operations"""
    storage = StorageManager()
    
    # Test saving a person with a conversation
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
    
    # Verify the data
    assert loaded_person.first_name == person.first_name, "First name mismatch"
    assert loaded_person.last_name == person.last_name, "Last name mismatch"
    assert loaded_person.email == person.email, "Email mismatch"
    assert len(loaded_conversations) == 1, "Conversation count mismatch"
    assert loaded_conversations[0].notes == conversation.notes, "Conversation notes mismatch"
    
    print("Storage tests passed successfully!")

def main():
    app = QApplication(sys.argv)
    
    # Run storage tests
    test_storage()
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()