from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QDateEdit,
    QTextEdit,
    QDialogButtonBox
)
from PyQt6.QtCore import QDate
from models import Conversation
from datetime import date

class ConversationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Conversation")
        self.setModal(True)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        # Date field (defaults to today)
        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDate(QDate.currentDate())
        
        # Notes field
        self.notes = QTextEdit()
        self.notes.setPlaceholderText("What did you talk about?")
        
        form.addRow("Date", self.date)
        form.addRow("Notes", self.notes)
        layout.addLayout(form)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_conversation(self) -> Conversation:
        return Conversation(
            date=self.date.date().toPyDate(),
            notes=self.notes.toPlainText().strip()
        ) 