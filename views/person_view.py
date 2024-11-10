from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QTextEdit,
    QGroupBox,
    QScrollArea,
    QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from models import Person, Conversation
from typing import List
from datetime import date

class ConversationWidget(QWidget):
    notesChanged = pyqtSignal(Conversation)  # Signal to notify when notes are edited
    
    def __init__(self, conversation: Conversation, parent=None):
        super().__init__(parent)
        self.conversation = conversation
        layout = QVBoxLayout(self)
        
        # Header with date and save button
        header_layout = QHBoxLayout()
        
        date_label = QLabel(conversation.date.strftime("%Y-%m-%d"))
        date_label.setStyleSheet("font-weight: bold;")
        header_layout.addWidget(date_label)
        
        save_button = QPushButton("Save")
        save_button.setEnabled(False)  # Initially disabled
        save_button.clicked.connect(self.save_notes)
        header_layout.addWidget(save_button)
        header_layout.addStretch()
        
        # Notes text area
        self.notes_text = QTextEdit()
        self.notes_text.setPlainText(conversation.notes)
        self.notes_text.setMaximumHeight(100)
        self.notes_text.textChanged.connect(lambda: save_button.setEnabled(True))
        
        layout.addLayout(header_layout)
        layout.addWidget(self.notes_text)
        
        self.save_button = save_button
    
    def save_notes(self):
        """Save the edited notes"""
        new_notes = self.notes_text.toPlainText().strip()
        if new_notes != self.conversation.notes:
            self.conversation.notes = new_notes
            self.notesChanged.emit(self.conversation)
            self.save_button.setEnabled(False)

class PersonView(QWidget):
    def __init__(self, storage_manager, parent=None):
        super().__init__(parent)
        self.storage = storage_manager
        self.current_person = None
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Person details section
        details_group = QGroupBox("Person Details")
        details_layout = QFormLayout()
        
        self.name_label = QLabel()
        self.email_label = QLabel()
        self.phone_label = QLabel()
        self.birth_date_label = QLabel()
        
        # Notes section with save button
        notes_container = QWidget()
        notes_layout = QVBoxLayout(notes_container)
        notes_layout.setContentsMargins(0, 0, 0, 0)
        
        notes_header = QHBoxLayout()
        notes_label = QLabel("Notes:")
        self.person_save_button = QPushButton("Save")
        self.person_save_button.setEnabled(False)
        self.person_save_button.clicked.connect(self.save_person_notes)
        notes_header.addWidget(notes_label)
        notes_header.addWidget(self.person_save_button)
        notes_header.addStretch()
        
        self.notes_text = QTextEdit()
        self.notes_text.setMaximumHeight(60)
        self.notes_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.notes_text.textChanged.connect(lambda: self.person_save_button.setEnabled(True))
        
        notes_layout.addLayout(notes_header)
        notes_layout.addWidget(self.notes_text)
        
        details_layout.addRow("Name:", self.name_label)
        details_layout.addRow("Email:", self.email_label)
        details_layout.addRow("Phone:", self.phone_label)
        details_layout.addRow("Birth Date:", self.birth_date_label)
        details_layout.addRow(notes_container)
        
        details_group.setLayout(details_layout)
        layout.addWidget(details_group)
        
        # Conversations section
        conversations_group = QGroupBox("Conversations")
        conversations_layout = QVBoxLayout()
        
        # Create a scroll area for conversations
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.conversations_widget = QWidget()
        self.conversations_layout = QVBoxLayout(self.conversations_widget)
        scroll.setWidget(self.conversations_widget)
        
        conversations_layout.addWidget(scroll)
        conversations_group.setLayout(conversations_layout)
        layout.addWidget(conversations_group)
    
    def display_person(self, person: Person, conversations: List[Conversation]):
        """Update the view with person and conversation data"""
        self.current_person = person
        
        # Update person details
        self.name_label.setText(person.full_name)
        self.email_label.setText(person.email or "")
        self.phone_label.setText(person.phone or "")
        self.birth_date_label.setText(person.birth_date.strftime("%Y-%m-%d") if person.birth_date else "")
        self.notes_text.setPlainText(person.notes or "")
        self.person_save_button.setEnabled(False)  # Reset save button state
        
        # Clear existing conversations
        while self.conversations_layout.count():
            child = self.conversations_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Sort conversations by date in reverse chronological order
        sorted_conversations = sorted(
            conversations,
            key=lambda x: x.date,
            reverse=True
        )
        
        # Add conversations
        for conv in sorted_conversations:
            conv_widget = ConversationWidget(conv)
            conv_widget.notesChanged.connect(self.save_conversation)
            self.conversations_layout.addWidget(conv_widget)
        
        # Add stretch to push conversations to the top
        self.conversations_layout.addStretch()
    
    def save_conversation(self, conversation: Conversation):
        """Save updated conversation back to storage"""
        if self.current_person and self.current_person.id:
            result = self.storage.load_person(self.current_person.id)
            if result:
                person, conversations = result
                
                # Update the matching conversation
                for conv in conversations:
                    if conv.id == conversation.id:
                        conv.notes = conversation.notes
                        break
                
                # Save back to storage
                self.storage.save_person(person, conversations)
    
    def save_person_notes(self):
        """Save updated person notes back to storage"""
        if self.current_person and self.current_person.id:
            result = self.storage.load_person(self.current_person.id)
            if result:
                person, conversations = result
                
                # Update person notes
                person.notes = self.notes_text.toPlainText().strip()
                
                # Save back to storage
                self.storage.save_person(person, conversations)
                self.person_save_button.setEnabled(False)