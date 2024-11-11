from PyQt6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QMessageBox,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QStyle
)
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QFont, QPalette, QColor
from models import Person
from .person_dialog import PersonDialog
from .conversation_dialog import ConversationDialog
from storage import StorageManager
from .person_view import PersonView

class PersonItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if not index.isValid():
            return
        
        # Get person and their conversations
        person = index.data(Qt.ItemDataRole.UserRole)
        result = self.parent().storage.load_person(person.id)
        if not result:
            return
        
        _, conversations = result
        
        # Find the most recent conversation
        last_conversation = None
        if conversations:
            last_conversation = max(conversations, key=lambda c: c.date)
        
        # Prepare the rectangle for drawing
        rect = option.rect
        
        # Handle selection highlighting
        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(rect, option.palette.highlight())
            painter.setPen(option.palette.highlightedText().color())
        else:
            painter.setPen(option.palette.text().color())
        
        # Draw the person's name
        name_font = QFont(option.font)
        name_font.setPointSize(10)
        painter.setFont(name_font)
        
        text_rect = QRect(rect.left() + 5, rect.top() + 5, 
                         rect.width() - 10, rect.height() // 2)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft, person.full_name)
        
        # Draw the last conversation date if exists
        if last_conversation:
            date_font = QFont(option.font)
            date_font.setPointSize(8)
            painter.setFont(date_font)
            
            if not option.state & QStyle.StateFlag.State_Selected:
                painter.setPen(QColor(100, 100, 100))  # Gray color for date
            
            date_rect = QRect(rect.left() + 5, text_rect.bottom(), 
                            rect.width() - 10, rect.height() // 2 - 5)
            date_text = f"Last contact: {last_conversation.date.strftime('%Y-%m-%d')}"
            painter.drawText(date_rect, Qt.AlignmentFlag.AlignLeft, date_text)
    
    def sizeHint(self, option, index):
        return QSize(option.rect.width(), 50)  # Fixed height for each item

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
        self.person_list.setItemDelegate(PersonItemDelegate(self))
        self.person_list.setSpacing(2)  # Add some space between items
        
        # Optional: Set alternating row colors
        self.person_list.setAlternatingRowColors(True)
        
        # Style the list widget
        self.person_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QListWidget::item {
                border-bottom: 1px solid #eee;
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
            QListWidget::item:alternate {
                background-color: #f8f8f8;
            }
        """)
        
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
        
        # Create and add person view to right panel
        self.person_view = PersonView(self.storage)
        self.person_view.conversationAdded.connect(self.on_conversation_added)
        self.right_panel.addWidget(self.person_view)
    
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
        self.new_conversation_action.setEnabled(False)
        selected_items = self.person_list.selectedItems()
        
        if selected_items:
            person = selected_items[0].data(Qt.ItemDataRole.UserRole)
            result = self.storage.load_person(person.id)
            
            if result:
                loaded_person, conversations = result
                self.person_view.display_person(loaded_person, conversations)
                self.new_conversation_action.setEnabled(True)
    
    def on_conversation_added(self):
        """Refresh the current person view when a conversation is added"""
        selected_items = self.person_list.selectedItems()
        if selected_items:
            self.on_person_selected()