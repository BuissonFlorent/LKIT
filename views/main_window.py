from PyQt6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QMessageBox
)
from PyQt6.QtCore import Qt
from models import Person
from .person_dialog import PersonDialog
from .conversation_dialog import ConversationDialog
from storage import StorageManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LKIT")
        self.setMinimumSize(800, 600)
        
        # Initialize storage first
        self.storage = StorageManager()
        
        # Create the central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create the left panel (will contain person list)
        self.person_list = QListWidget()
        self.person_list.setMaximumWidth(250)
        
        # Create the right panel (will contain stacked widgets for different views)
        self.right_panel = QStackedWidget()
        
        # Add panels to the main layout
        main_layout.addWidget(self.person_list)
        main_layout.addWidget(self.right_panel)
        
        # Setup the menu bar
        self._create_menu_bar()
        
        # Load existing persons
        self.load_persons()
        
        # Connect list selection
        self.person_list.itemSelectionChanged.connect(self.on_person_selected)
    
    def _create_menu_bar(self):
        """Create the main window's menu bar"""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        
        # Add Person action
        new_person_action = file_menu.addAction("New Person")
        new_person_action.triggered.connect(self.add_person)
        
        # Add Conversation action (disabled by default)
        self.new_conversation_action = file_menu.addAction("New Conversation")
        self.new_conversation_action.triggered.connect(self.add_conversation)
        self.new_conversation_action.setEnabled(False)
        
        # Add separator and Exit action
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
    
    def load_persons(self):
        """Load all persons from storage"""
        self.person_list.clear()
        for person in self.storage.get_all_persons():
            item = QListWidgetItem(person.full_name)
            item.setData(Qt.ItemDataRole.UserRole, person)
            self.person_list.addItem(item)
    
    def add_person(self):
        dialog = PersonDialog(parent=self)
        if dialog.exec():
            person, conversation = dialog.get_data()
            conversations = [conversation] if conversation else []
            
            # Save to storage
            self.storage.save_person(person, conversations)
            
            # Refresh the list
            self.load_persons()
    
    def add_conversation(self):
        """Add a conversation to the selected person"""
        selected_items = self.person_list.selectedItems()
        if not selected_items:
            return
            
        person = selected_items[0].data(Qt.ItemDataRole.UserRole)
        
        dialog = ConversationDialog(self)
        if dialog.exec():
            conversation = dialog.get_conversation()
            if self.storage.add_conversation(person.id, conversation):
                QMessageBox.information(self, "Success", "Conversation added successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to add conversation")
    
    def on_person_selected(self):
        """Handle person selection"""
        self.new_conversation_action.setEnabled(bool(self.person_list.selectedItems()))