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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LKIT")
        self.setMinimumSize(800, 600)
        
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
        
        # Add some dummy data for testing
        self._add_test_data()
    
    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        new_person_action = file_menu.addAction("New Person")
        new_person_action.triggered.connect(self.add_person)
        file_menu.addAction("Exit")
        
        # Edit menu
        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction("Settings")
    
    def _add_test_data(self):
        test_persons = [
            Person(first_name="John", last_name="Doe"),
            Person(first_name="Jane", last_name="Smith"),
            Person(first_name="Robert", last_name="Johnson")
        ]
        
        for person in test_persons:
            item = QListWidgetItem(person.full_name)
            item.setData(Qt.ItemDataRole.UserRole, person)
            self.person_list.addItem(item)
    
    def add_person(self):
        dialog = PersonDialog(parent=self)
        if dialog.exec():
            person = dialog.get_person_data()
            item = QListWidgetItem(person.full_name)
            item.setData(Qt.ItemDataRole.UserRole, person)
            self.person_list.addItem(item)