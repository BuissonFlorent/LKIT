from PyQt6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QListWidget,
    QStackedWidget
)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LKIT")
        self.setMinimumSize(800, 600)
        
        # Create the central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create the left panel (will contain contact list)
        self.contact_list = QListWidget()
        self.contact_list.setMaximumWidth(250)
        
        # Create the right panel (will contain stacked widgets for different views)
        self.right_panel = QStackedWidget()
        
        # Add panels to the main layout
        main_layout.addWidget(self.contact_list)
        main_layout.addWidget(self.right_panel)
        
        # Setup the menu bar
        self._create_menu_bar()
        
        # Add some dummy data for testing
        self.contact_list.addItems([
            "John Doe",
            "Jane Smith",
            "Bob Johnson"
        ])
    
    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction("New Contact")
        file_menu.addAction("Exit")
        
        # Edit menu
        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction("Settings")