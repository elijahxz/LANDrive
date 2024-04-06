
import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, \
                            QLabel, QLineEdit, QVBoxLayout, QWidget, \
                            QMenu

""" 
    Most of the PyQt6 documentation I found from a tutorial here:
        https://www.pythonguis.com/pyqt6-tutorial/
"""

# Notes:
#super().mousePressEvent(event)
# e.accept() marks an event as handled
# e.ignore() marks an event as unhandled


# Subclass QMainWindow - Customize main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window Setup 
        self.setWindowTitle("LANDrive")
        self.setMinimumSize(800,500)
      

        # Header Setup
        self.header = QLabel("LANDrive")
        
        font = self.header.font()
        font.setPointSize(50)
        self.header.setFont(font)
        
        self.header.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)


        # Button Setup
        self.button = QPushButton(text="Connect", parent=self)
        
        self.button.clicked.connect(self.onClick)
        self.button.setObjectName("connect") 
        self.button.setFixedSize(500, 200)
    
        button_font = self.button.font()
        button_font.setPointSize(35)
        self.button.setFont(button_font)
        
        #self.button.setObjectName("connect")


        # Label Setup
        self.label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.header)
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter) 


        # Container Setup
        container = QWidget()
        container.setLayout(layout)
        

        # Set the central widget of the Window.
        self.setCentralWidget(container)
    
    def onClick(self):
        self.label.setText("Connecting...")
   
    # used for right clicking on the mouse
    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("Exit Program", self))
        context.exec(e.globalPos()) 


# Display the GUI to the user
app = QApplication([])
window = MainWindow()
window.show()

app.exec()

