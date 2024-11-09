from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDateEdit,
    QTextEdit,
    QDialogButtonBox,
    QWidget,
    QGroupBox
)
from PyQt6.QtCore import Qt, QDate
from models import Person, Conversation
from datetime import date
from typing import Optional

class PersonDialog(QDialog):
    def __init__(self, person=None, parent=None):
        super().__init__(parent)
        self.person = person
        self.setWindowTitle("Add Person" if person is None else "Edit Person")
        self.setModal(True)
        self.setup_ui()
        
        if person:
            self.populate_fields()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create form layout for the person details
        form = QFormLayout()
        
        # Create input fields
        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.email = QLineEdit()
        self.phone = QLineEdit()
        
        self.birth_date = QDateEdit()
        self.birth_date.setCalendarPopup(True)
        self.birth_date.setSpecialValueText(" ")
        self.birth_date.setDate(self.birth_date.minimumDate())
        
        self.notes = QTextEdit()
        self.notes.setMaximumHeight(100)
        
        # Add person fields to form
        form.addRow("First Name *", self.first_name)
        form.addRow("Last Name *", self.last_name)
        form.addRow("Email", self.email)
        form.addRow("Phone", self.phone)
        form.addRow("Birth Date", self.birth_date)
        form.addRow("Notes", self.notes)
        
        layout.addLayout(form)
        
        # Create conversation group
        conversation_group = QGroupBox("Add Conversation")
        conversation_layout = QFormLayout()
        
        self.conversation_date = QDateEdit()
        self.conversation_date.setCalendarPopup(True)
        self.conversation_date.setDate(QDate.currentDate())  # Default to today
        
        self.conversation_notes = QTextEdit()
        self.conversation_notes.setMaximumHeight(100)
        self.conversation_notes.setPlaceholderText("What did you talk about?")
        
        conversation_layout.addRow("Date", self.conversation_date)
        conversation_layout.addRow("Notes", self.conversation_notes)
        
        conversation_group.setLayout(conversation_layout)
        layout.addWidget(conversation_group)
        
        # Add buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def populate_fields(self):
        """Fill the form with existing person data"""
        self.first_name.setText(self.person.first_name)
        self.last_name.setText(self.person.last_name)
        self.email.setText(self.person.email or "")
        self.phone.setText(self.person.phone or "")
        if self.person.birth_date:
            self.birth_date.setDate(self.person.birth_date)
        self.notes.setPlainText(self.person.notes or "")
    
    def get_data(self) -> tuple[Person, Optional[Conversation]]:
        """Create Person and Conversation objects from the form data"""
        birth_date = None if self.birth_date.date() == self.birth_date.minimumDate() else self.birth_date.date().toPyDate()
        
        person = Person(
            id=getattr(self.person, 'id', None),
            first_name=self.first_name.text().strip(),
            last_name=self.last_name.text().strip(),
            email=self.email.text().strip() or None,
            phone=self.phone.text().strip() or None,
            birth_date=birth_date,
            notes=self.notes.toPlainText().strip() or None,
        )
        
        # Create conversation only if notes are provided
        conversation = None
        if self.conversation_notes.toPlainText().strip():
            conversation = Conversation(
                date=self.conversation_date.date().toPyDate(),
                notes=self.conversation_notes.toPlainText().strip()
            )
        
        return person, conversation