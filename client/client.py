import time
import socket
import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, \
                            QLabel, QLineEdit, QVBoxLayout, QWidget, \
                            QMenu, QStackedWidget, QHBoxLayout

""" 
    Most of the PyQt6 documentation I found from a tutorial here:
        https://www.pythonguis.com/pyqt6-tutorial/
"""

# Notes:
#super().mousePressEvent(event)
# e.accept() marks an event as handled
# e.ignore() marks an event as unhandled
# css styling
# connect_button.setObjectName("connect")
    

# This app does not ask the client to insert a port, 
# so the server and client always tries to access
# 8504 on localhost
HOST = "127.0.0.1"
PORT = 8504
CLOSE_CONNECTION = "TerminateTCPConnection"

"""
    I personally think this style of coding is ugly, but this sets up the window with 
    the connect screen, and the main screen.
"""
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a socket for the client  
        self.c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CONNECTING = False

        """
            Start of GUI initialization
        """
        # Window Setup 
        self.setWindowTitle("LANDrive")
        self.setMinimumSize(1024,768)


        # Set exit program option on the context menu
        self.context_menu = QMenu(self)
        action1 = self.context_menu.addAction("Exit Program")
        action1.triggered.connect(QApplication.quit)
      

        # Connect screen setup
        self.connect_widget = QWidget()
        
        # Allows class to see this because multiple functions access it
        self.connect_label = QLabel()
        
        self.setupConnectScreen()


        # Main screen setup
        self.main_widget = QWidget()
        
        self.setupMainScreen()


        # Container Setup
        self.container = QStackedWidget()
        self.container.addWidget(self.connect_widget)
        self.container.addWidget(self.main_widget) 

        self.setCentralWidget(self.container)
        
        self.container.setCurrentWidget(self.connect_widget)

        """
            End of GUI initialization
        """
    
    """ 
        Two screens cant share elements, so we have to create 
        Multiple objects, even if they share the same properties
        PyQt also allows series classes, but this works fine.
    """
    def createHeader(self, name):
        header = QLabel(name)
        
        font = header.font()
        font.setPointSize(50)
        header.setFont(font)
        
        header.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        
        return header

    def setupConnectScreen(self):
        # Connect Button
        connect_button = QPushButton(text="Connect", parent=self)
        connect_layout = QVBoxLayout()
        
        connect_button.clicked.connect(self.connectToServer)
        connect_button.setObjectName("connect") 
        connect_button.setFixedSize(500, 200)
    
        button_font = connect_button.font()
        button_font.setPointSize(35)
        connect_button.setFont(button_font)
        
        # Layout Setup
        connect_layout.addWidget(self.createHeader("LANDrive"))
        connect_layout.addWidget(connect_button)
        connect_layout.addWidget(self.connect_label)
        connect_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter) 
       
        # Add layout to the widget
        self.connect_widget.setLayout(connect_layout)
       
        return

    def setupMainScreen(self):
        main_layout = QVBoxLayout()
        main_top_layout = QHBoxLayout()
        main_middle_layout = QHBoxLayout()
        main_bottom_layout = QHBoxLayout()
        
        main_top_layout.addWidget(self.createHeader("LANDrive"))

        main_layout.addLayout(main_top_layout)
        main_layout.addLayout(main_middle_layout)
        main_layout.addLayout(main_bottom_layout)
        
        self.main_widget.setLayout(main_layout)

        return

    """ Called when the GUI is closed """
    def closeEvent(self, event):
        event.accept()
        # Always try to close the socket when the user closes the application
        try:
            self.c_socket.send(CLOSE_CONNECTION.encode())
            self.c_socket.close()
        except Exception:
            pass

    """ Used for right clicking on the mouse """
    def contextMenuEvent(self, e):
        self.context_menu.exec(e.globalPos()) 
   
    """ 
        Connect button event, trys to connect to the server 
        NOTE: The time.sleep() functions just make the UI look
              a little better ... since we are connecting to 
              localhost its super fast
    """
    def connectToServer(self):
        
        # We cant allow the user to spam the connect button,
        # or else the program will crash :)
        if self.CONNECTING:
            return

        # Force non-async update for the connecting... message
        self.connect_label.setText("Connecting...")
        self.connect_label.repaint()
        time.sleep(1)

        try:
            self.CONNECTING = True
            
            # Pass in a tuple to connect()
            self.c_socket.connect((HOST, PORT))
        except ConnectionRefusedError:
            self.connect_label.setText("Error: Connection to server refused. " + 
                               "Please try again or check the server status")
            self.CONNECTING = False
            return
        self.CONNECTING = False
        self.connect_label.setText("Success! Connected to the server!")
        self.connect_label.repaint()
        
        time.sleep(2)

        self.displayMainScreen()
    
    def displayMainScreen(self):
        # Hide connection and show the main widget
        self.connect_label.setText("")
        self.container.setCurrentWidget(self.main_widget)


def main():
    # Display the GUI to the user
    app = QApplication([])
    window = MainWindow()
    window.show()

    app.exec()

main()
