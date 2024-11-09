import sys
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow
from storage import StorageManager
from models import Person, Conversation
from datetime import date

def test_storage():
    storage = StorageManager()
    
    # Create test person with a conversation
    person = Person(
        first_name="John",
        last_name="Doe",
        email="john@example.com"
    )
    
    conversation = Conversation(
        date=date.today(),
        notes="First meeting"
    )
    
    # Save person
    storage.save_person(person, [conversation])
    print(f"Saved person with ID: {person.id}")
    
    # Load person
    loaded_person, loaded_conversations = storage.load_person(person.id)
    print(f"Loaded person: {loaded_person.full_name}")
    print(f"First conversation: {loaded_conversations[0].notes}")
    
    # Get all persons
    all_persons = storage.get_all_persons()
    print(f"Total persons: {len(all_persons)}")

def main():
    app = QApplication(sys.argv)
    
    # Test storage
    test_storage()
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()