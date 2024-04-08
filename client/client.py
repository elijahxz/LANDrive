import json
import time
import socket
import sys

# Whew, thats alot.
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QMainWindow, QPushButton, QSizePolicy, QStackedWidget,
    QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout,
    QWidget, QMenu, QStyleFactory)

"""  
    Ui_Mainwindow is the barebones GUI I created in QT Developer
    I tried making one using my own code, but take a look in UserInterface.py and 
    you'll see why I used the tool instead :) ... It's a nightmare to program. 
"""
from UserInterface import Ui_MainWindow

# This app does not ask the client to insert a port,
# so the server and client always tries to access
# 8504 on localhost
HOST = "127.0.0.1"
PORT = 8504

MAX_SIZE = 16384

CLOSE_CONNECTION = "TerminateTCPConnection"
REFRESH = "RefreshFiles"

# QT Developer chose these. To change the screen, use we
# self.ui.stackedWidget.setCurrentIndex(3)
CONNECT_SCREEN = 0
MAIN_SCREEN = 1
EDIT_SCREEN = 2

""" 
   The window is a wrapper class for Ui_MainWindow so we can interact with it. 
"""
class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        # Used for connecting to the server 
        self.CONNECTING = False

        self.THEMES = QStyleFactory.keys()
        self.current_theme = app.style().name()

        # Create a socket for the client
        self.c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        # Initialize the other class and set everything up
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setupUiFunctionality()


        # Set exit program option on the context menu
        self.context_menu = QMenu(self)
        action1 = self.context_menu.addAction("Change Theme")
        action1.triggered.connect(self.changeTheme)
        action2 = self.context_menu.addAction("Exit Program")
        action2.triggered.connect(QApplication.quit)
   
    def setupUiFunctionality(self):
        self.ui.connect_button.clicked.connect(self.connectToServer)
        self.ui.disconnect_button.clicked.connect(self.disconnectFromServer)
        

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

    
    # Changes the theme of the app (called by a menuevent)
    def changeTheme(self):
        counter = 0
        length = len(self.THEMES) - 1
        
        if (length < 0):
            return
        
        for theme in self.THEMES: 
            if self.current_theme == theme:
                break
            counter += 1
        
        counter += 1
        if counter > length: 
            counter = 0

        self.current_theme = self.THEMES[counter] 
        app.setStyle(self.current_theme)
        return

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
        self.ui.connect_label.setText("Connecting...")
        self.ui.connect_label.repaint()
        time.sleep(1)

        try:
            self.CONNECTING = True

            # Pass in a tuple to connect()
            self.c_socket.connect((HOST, PORT))
        except ConnectionRefusedError:
            self.ui.connect_label.setText("Error: Connection to server refused. " +
                               "Please try again or check the server status")
            self.CONNECTING = False
            return
        self.CONNECTING = False
        self.ui.connect_label.setText("Success! Connected to the server!")
        self.ui.connect_label.repaint()

        time.sleep(2)

        self.displayMainScreen()

    def disconnectFromServer(self):
        self.c_socket.send(CLOSE_CONNECTION.encode())
        self.c_socket.close()

        self.c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.displayConnectScreen()
    
    def displayMainScreen(self):
        # Hide connection and show the main widget
        self.ui.connect_label.setText("")
        self.ui.stackedWidget.setCurrentIndex(MAIN_SCREEN)

    def displayConnectScreen(self):
        self.ui.stackedWidget.setCurrentIndex(CONNECT_SCREEN)

    def fetchServerFiles(self):
        self.c_socket.send("RefreshFiles".encode())

        data = self.c_socket.recv(MAX_SIZE)
        data = data.decode("utf-8")

        files = json.loads(data)

        return files






app = QApplication([])
window = Window()
window.show()

app.exec()
