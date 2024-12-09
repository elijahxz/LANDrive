import json
import os
from pathlib import Path
import pickle
import socket
import struct
import sys
import tempfile
import time
from datetime import datetime
from threading import Lock
import platformdirs
import struct
from shared import *

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
    QWidget, QMenu, QStyleFactory, QFileDialog, QMessageBox, QInputDialog
)

"""  
    Ui_Mainwindow is the barebones GUI I created in QT Developer
    I tried making one using my own code, but take a look in UserInterface.py and 
    you'll see why I used the tool instead :) ... It's a nightmare to program. 
"""
from UserInterface import Ui_MainWindow
from Upload import Ui_Form

""" Mutex for accessing the self.files list in the Window Class """
fileMutex = Lock()

"""
    QT Developer chose these. To change the screen, use we
    self.ui.stackedWidget.setCurrentIndex(3)
"""
CONNECT_SCREEN = 0
MAIN_SCREEN = 1
EDIT_SCREEN = 2

"""
    This window is a popup that is displayed when a user
    uploads files from their local machine or downloads a 
    directory from the server
"""
class StatusWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.window = False
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.closeBtn.clicked.connect(self.closeCustomEvent)

    def downloadWindow(self):
        self.setWindowTitle("Directory Download Status")
        self.ui.label.setText("Download Status")

    def setEnableWindow(self, window):
        self.window = window
    
    def updateScreen(self, string, done):
        # Force non-async update for the update
        self.ui.files.setText(string)
        self.ui.files.repaint()
    
    def closeCustomEvent(self):
        self.window.ui.stackedWidget.setEnabled(True)
        self.hide()

    def closeEvent(self, event):
        self.window.ui.stackedWidget.setEnabled(True)
        event.accept()
        self.close()


""" 
   The window is a wrapper class for Ui_MainWindow so we can interact with it.
   This class is very long and holds all of the functionality for the UI
"""
class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        
        self.PUBLIC_KEY = None
        self.PRIVATE_KEY = None
        self.S_PUBLIC_KEY = None


        # Used to save the last host inputted by the user
        self.APPLICATIONDATA = None
        self.LASTHOST = None

        # Used for connecting to the server 
        self.CONNECTING = False
       
        # Used to detect if the user is editing a file
        self.EDITING = False
        
        # Keep track of how far the user goes down the file tree
        self.dir_stack = [BASE_DIR]
        
        # This is used to keep track of the files on the server's side
        self.files = list()
        
        # Contains the themes for the application
        self.THEMES = QStyleFactory.keys()
        self.current_theme = app.style().name()
           
        # Contains which file is selected by the user at any given time
        self.current_selection = None

        # When CTRL is active, push files to this list
        self.current_selection_list = list()

        # Create a socket for the client
        self.c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Initialize the other class and set everything up
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setupUiFunctionality()

        self.CTRL = False
        
        # Setup the exit program & change theme option for the context menu
        self.context_menu = QMenu(self)
        action1 = self.context_menu.addAction("Change Theme")
        action1.triggered.connect(self.changeTheme)
        action2 = self.context_menu.addAction("Exit Program")
        action2.triggered.connect(QApplication.quit)
       
        my_icon = QIcon()
        my_icon.addFile('folder-icon.png')
        self.setWindowIcon(my_icon)
        
        self.initiate_file()

    def initiate_file(self): 
        # Find the appropriate directory for storing app-specific data
        app_name = "LANDrive"

        # Get the user data directory in a cross-platform way
        data_dir = platformdirs.user_data_dir(app_name)

        # Ensure the directory exists
        Path(data_dir).mkdir(parents=True, exist_ok=True)

        # Define the path to the host file
        hosts_file_path = os.path.join(data_dir, 'lasthost')
        
        self.APPLICATIONDATA = hosts_file_path

        # Check if the 'hosts' file exists
        if os.path.exists(hosts_file_path):
            with open(hosts_file_path, 'r') as file:
                server_name = file.readline().strip()
                port = file.readline().strip()
                self.ui.server_name.setText(server_name)
                self.ui.port_number.setText(port)

    """ Check if CTRL has been pressed """
    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            self.CTRL = True
            print("START")
            self.ui.tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)

    """ Check if CTRL has been released """
    def keyReleaseEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.NoModifier:
            self.CTRL = False
            self.ui.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

    """ Sets up all of the button functionality and click events """
    def setupUiFunctionality(self):
        self.ui.connect_button.clicked.connect(self.connectToServer)
        self.ui.disconnect_button.clicked.connect(self.disconnectFromServer)
        self.ui.disconnect_2.clicked.connect(self.disconnectFromServerWhileEditing)
        self.ui.back.clicked.connect(self.dirUp)
        self.ui.refresh.clicked.connect(self.refreshFiles)
        self.ui.upload.clicked.connect(self.selectFile)
        self.ui.download.clicked.connect(self.downloadFile)
        self.ui.edit.clicked.connect(self.editFile)
        self.ui.cancel.clicked.connect(self.editCancel)
        self.ui.save.clicked.connect(self.editSave)
        self.ui.delete_2.clicked.connect(self.deleteFile)
        self.ui.create_dir.clicked.connect(self.createDirectory)
        
        # Selecting a row calls an event handler
        self.ui.tableWidget.doubleClicked.connect(self.dirDown)
        self.ui.tableWidget.clicked.connect(self.currentSelection)
        
        self.PUBLIC_KEY, self.PRIVATE_KEY = generate_rsa_keys()

    """ Called when the GUI is closed """
    def closeEvent(self, event):
        event.accept()
        
        # If we are editing a file, let the server know we are done
        if self.EDITING:
            self.editCancel()

        # Always try to close the socket when the user closes the application
        try:
            
            send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.SUCCESS.encode())

            send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.CLOSE_CONNECTION.encode())
            self.c_socket.close()
        except Exception:
            pass


    """ Used for right clicking on the mouse """
    def contextMenuEvent(self, e):
        self.context_menu.exec(e.globalPos())


    """ Changes the theme of the app (called by a menuevent) """
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


    """
        Connect button event, trys to connect to the server
        NOTE: The time.sleep() functions just make the UI look
              a little better ...
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

            # Get the user specified server name and port
            server = self.ui.server_name.text()
            port = self.ui.port_number.text()
            
            # Check validity
            if server == "" or port == "" or not port.isdigit():
                self.CONNECTING = False
                self.ui.connect_label.setText("Invalid server or port, please try again")
                self.ui.connect_label.repaint()
                return
            
            # Convert to int
            port = int(port)
            
            # Check port validity
            if port <= 0 or port >= 65536:
                self.CONNECTING = False
                self.ui.connect_label.setText("Invalid port (1-65535), please try again")
                self.ui.connect_label.repaint()
                return

            # localhost should be represented by 127.0.0.1 .... I think 
            if server.lower() == "localhost":
                server = "127.0.0.1"

            # Pass in a tuple to connect()
            self.c_socket.connect((server, port))

        except ConnectionRefusedError:
            self.ui.connect_label.setText("Error: Connection to server refused. " +
                               "Please check inputs and try again or check the server status")
            self.CONNECTING = False
            return
        
        # Get the server's public key and send out client public key.
        print("Getting key", flush = True)
        self.S_PUBLIC_KEY = recieve_key(self.c_socket)
        
        send_key(self.c_socket, self.PUBLIC_KEY)
        
        print("Done with key exchange!", flush = True) 
        data = recieve_data(self.c_socket)

        print("Sending Success Message!", flush = True) 
        send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.SUCCESS.encode())
        
        self.CONNECTING = False
        self.ui.connect_label.setText("Success! Connected to the server!")
        self.ui.connect_label.repaint()

        time.sleep(2)
        
        with open(self.APPLICATIONDATA, 'w') as file:
            file.write(server + "\n")
            file.write(str(port) + "\n")

        self.displayMainScreen()


    """ If we try to disconnect while editing a file, let the server know """
    def disconnectFromServerWhileEditing(self):
        self.editCancel()
        self.disconnectFromServer()


    """ Disconnects from the server and shows the connect screen """
    def disconnectFromServer(self):
        send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.CLOSE_CONNECTION.encode())
        self.c_socket.close()

        self.c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.displayConnectScreen()


    """ Sets up the main screen to be displayed """
    def displayMainScreen(self):
        # Hide connection and show the main widget
        self.ui.connect_label.setText("")
       
        self.dir_stack = [BASE_DIR]

        self.fetchServerFiles()
        
        self.fillTable()

        self.ui.stackedWidget.setCurrentIndex(MAIN_SCREEN)


    """ Shows the connect screen """
    def displayConnectScreen(self):
        self.ui.stackedWidget.setCurrentIndex(CONNECT_SCREEN)
    

    def currentSelectionListProcess(self, func):
        selections = self.current_selection_list
        self.current_selection_list = list()
        
        for selection in selections:
            self.current_selection = selection
            func()
        
        self.current_selection = None

    """ 
        Called when a table element is clicked
        This is stored in a variable for future functionality
    """
    def currentSelection(self, element):
        current_selection = self.ui.tableWidget.item(element.row(), 0).text()

        # When a file is selected using ctrl, append it to this list
        if self.CTRL:
            # Check if the previous selected item is in the list. 
            # This is required to make sense on the GUI
            if self.current_selection is not None and not self.current_selection in self.current_selection_list:
                self.current_selection_list.append(self.current_selection)

            # Add current selection to the list
            if not current_selection in self.current_selection_list:
                self.current_selection_list.append(current_selection)
            # If the user selects the same row again, it un-highlights it, 
            # so remove it from the list
            else:
                self.current_selection_list.remove(current_selection)

        else:
            self.current_selection_list = list()
        
        self.current_selection = current_selection
       

    """ Gets the relative path for the server directory that is shown on the screen """
    def currentServerPath(self):
        path = ""
        for folder in self.dir_stack:
            path += folder + "/"
        
        return path


    """ Refreshes the server's files """
    def refreshFiles(self):
        self.fetchServerFiles()
        self.fillTable()


    """ Used to recieve a file, this gets the struct that is sent before the actual file """
    def recieveDataSize(self):
        fmt = "<Q"
        expected_bytes = struct.calcsize(fmt)
        recieved_bytes = 0
        stream = bytes()

        while recieved_bytes < expected_bytes:
            chunk = self.c_socket.recv(expected_bytes - recieved_bytes)
            stream += chunk
            recieved_bytes += len(chunk)
        
        datasize = struct.unpack(fmt, stream)[0]
        return datasize


    """ 
        Recieves data from the server (used in self.fetchServerFiles) 
        Similar to recieveFile.
    """
    def recieveData(self):
        # First read from the socket the amount of
        # bytes that will be recieved from the server.
        datasize = self.recieveDataSize()

        recieved_bytes = 0
        data = bytes()
        # recieve the data in 1024-bytes chunks
        # until reaching the total amount of bytes
        # that was informed by the server.
        while recieved_bytes < datasize:
            chunk = self.c_socket.recv(MAX_SIZE)
            if chunk:
                recieved_bytes += len(chunk)
                data = data + chunk
        
        return data


    """ 
        Recieves a file from the server and saves it to the specified filename 
        Similar to RecieveData.
    """
    def recieveFile(self, filename):
        # First read from the socket the amount of
        # bytes that will be recieved from the file.
        #filesize = self.recieveDataSize()
        
        file = recieve_data(self.c_socket)
        
        # Open a new file where to store the recieved data.
        with open(filename, "wb") as f:
            #recieved_bytes = 0
            # recieve the file data in 1024-bytes chunks
            # until reaching the total amount of bytes
            # that was informed by the client.
            #while recieved_bytes < filesize:
            #    chunk = self.c_socket.recv(MAX_SIZE)
            #    if chunk:
            #        recieved_bytes += len(chunk)
            #        f.write(chunk)
            f.write(file)

    """ Gets the current version of the server files from the server """
    def fetchServerFiles(self):
     
        # Lock down the file mutex so we can refresh
        with fileMutex:
            send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.REFRESH.encode())
            #data = self.recieveData()
            data = recieve_data(self.c_socket)

            # We assume no error when pickling the file, but there 
            # should be a try/catch block here...TODO for the future
            self.files = pickle.loads(data)
      
        # Get the refresh time and display it
        now = datetime.now()
        date_string = now.strftime("%H:%M:%S")
        
        self.ui.updated.setText("Last Updated: " + date_string)
        self.ui.updated.repaint()
        
        # Request the number of users connected to the server
        send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.USERS.encode())
        
        #data = self.c_socket.recv(MAX_SIZE)
        data = recieve_data(self.c_socket)
        
        users = data.decode()
       
        # Updates main screen
        self.ui.users.setText("Users: " + users)
        self.ui.users.repaint()

        # Updates the file editing screen
        self.ui.users_2.setText("Users: " + users)
        self.ui.users_2.repaint()

        
    """ Clears the table that shows the files (used during refresh & traversal) """
    def clearTable(self):
        while (self.ui.tableWidget.rowCount() > 0):
            self.ui.tableWidget.removeRow(0)


    """ Fills the table that shows the files (used during refresh & traversal) """
    def fillTable(self):
        row = 0
        dir_files = list()
        
        self.clearTable()

        # Update which directory we are in for every refresh
        current_dir = self.dir_stack[ (len(self.dir_stack) - 1) ]
        self.ui.dir_name.setText("Directory: " + current_dir)
        self.ui.dir_name.repaint()

        # Lock down the mutex and check which files are in the directory we are currently in
        with fileMutex:
            for file in self.files:
                if file.current_dir == current_dir:
                    dir_files.append(file)
       
        # No files in the directory
        if len(dir_files) == 0:
            self.ui.tableWidget.setRowCount(1)
            one = QTableWidgetItem("No Files In This Folder")
            two = QTableWidgetItem("")
            three = QTableWidgetItem("")
            
            # Makes the row not selectable/editable
            one.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            two.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            three.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )

            self.ui.tableWidget.setItem(row, 0, one)         
            self.ui.tableWidget.setItem(row, 1, two)         
            self.ui.tableWidget.setItem(row, 2, three)
        
        # Display the files in the directory to the user
        else:
            self.ui.tableWidget.setRowCount(len(dir_files))
            for file in dir_files:
                one = QTableWidgetItem(file.name)
                two = QTableWidgetItem(file.time_stamp)
                three = QTableWidgetItem(file.size)

                # Makes the row not selectable/editable
                one.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
                two.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
                three.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
                
                self.ui.tableWidget.setItem(row, 0, one)         
                self.ui.tableWidget.setItem(row, 1, two)         
                self.ui.tableWidget.setItem(row, 2, three)
                row += 1


    """ Checks if directory passed in exists on the server """ 
    def checkIfDirectoryExists(self, directory):
        valid_selection = False
        
        self.refreshFiles()
        
        with fileMutex:
            for file in self.files:
                if file.directory_flag == True and file.name == directory: 
                    valid_selection = True
                    break

        if directory == BASE_DIR: 
            valid_selection = True

        return valid_selection


    """ 
        When another user deletes a directory that we are currently in, this
        function takes us back to a directory that still exists.
    """
    def goToValidDirectory(self):
        valid = False
        
        self.refreshFiles()

        while not valid:
            self.dir_stack.pop()
            dir_num = len(self.dir_stack) - 1
            
            if dir_num >= 0:
                valid = self.checkIfDirectoryExists(self.dir_stack[dir_num])
            # Base directory will always be valid
            else:
                valid = True
        
        # When we are in a valid directory, refresh the files and show them to the user
        self.refreshFiles()


    """ Go down a directory """
    def dirDown(self, element):
        valid_selection = False
        
        # Since we are in a new directory, remove the current selection
        self.current_selection = None
        
        new_dir = self.ui.tableWidget.item(element.row(), 0).text()
                
        # Check the directory we are in
        dir_num = len(self.dir_stack) - 1
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Status")
        
        if dir_num >= 0:
            # Check if the directory we are in is still valid
            valid_dir = self.checkIfDirectoryExists(self.dir_stack[dir_num])
            
            if not valid_dir: 
                msg.setText("This directory does not exist anymore, " +
                            "backing up to a directory that exists")
                
                self.goToValidDirectory()
                msg.exec()
                return
               
        # Check whether the selection is valid (if its a directory or not)
        with fileMutex:
            for file in self.files:
                if file.directory_flag == True and file.name == new_dir: 
                    valid_selection = True
                    break
        
        if not valid_selection:
            return
            
        # Check if the directory we are in is still valid
        valid_dir = self.checkIfDirectoryExists(self.dir_stack[dir_num])
        
        if not valid_dir: 
            msg.setText("This directory does not exist anymore, " +
                        "backing up to a directory that exists")
            
            self.goToValidDirectory()
            msg.exec()
            return 
        
        self.dir_stack.append(new_dir)

        self.refreshFiles()


    """ Go up to the next directory """
    def dirUp(self):
        # Since we are in a new directory, remove the current selection
        self.current_selection = None
        
        directory = len(self.dir_stack) - 1
        
        if (directory <= 0):
            return

        self.dir_stack.pop()
        
        # Check the directory we are in
        dir_num = len(self.dir_stack) - 1
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Status")
        
        # Check if the directory we are in is still valid
        valid_dir = self.checkIfDirectoryExists(self.dir_stack[dir_num])
        
        if not valid_dir: 
            msg.setText("This directory does not exist anymore, " +
                        "backing up to a directory that exists")
            self.goToValidDirectory()
            msg.exec()
            return 

        self.refreshFiles()


    """ Requests to create a new directory on the server """
    def createDirectory(self):
        text, ok = QInputDialog.getText(self, 
                                         "Directory Name", 
                                         "Enter desired directory name:"
                                         )
       
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Status")
        
        if ok:
            # Check the directory we are in
            dir_num = len(self.dir_stack) - 1
            if dir_num >= 0:
                if self.dir_stack[dir_num] == text:
                    msg.setText("Error: can not create folder with same name " +
                                "as parent folder. Please choose a different name " +
                                "and try again")
                    msg.exec()
                    return

            send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.CREATE_DIR.encode())
                
            #response = self.c_socket.recv(MAX_SIZE)
            response = recieve_data(self.c_socket)
            if response.decode() != ResponseCode.READY:
                msg.setText("There was an error on the server's side, " +
                            "Please refresh and try again!")
                msg.exec()
                return
            
            path = self.currentServerPath() + text

            send_data(self.c_socket, self.S_PUBLIC_KEY, path.encode())
            
            #response = self.c_socket.recv(MAX_SIZE)
            response = recieve_data(self.c_socket)

            if response.decode() == ResponseCode.SUCCESS:
                msg.setText("Success!!!")
            elif response.decode() == ResponseCode.DUPLICATE:
                msg.setText("Error: Duplicate directory found!")
            else:
                msg.setText("Error: Could not create directory.\nNote: unique directory " +
                            "names are requred.")
            
            msg.exec()
            self.refreshFiles()  


    """ Selects files from the user and uploads them to the server """
    def selectFile(self):
        files = list()

        # I believe this should work for MAC, but untested.
        default_dir = os.path.expanduser('~/Documents')
        
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        dlg.setDirectory(default_dir)
        
        if dlg.exec():
            files = dlg.selectedFiles()
            
            file_info = ""
            self.window = StatusWindow()
            self.window.setEnableWindow(self) 
            
            with fileMutex:
                results = self.uploadFiles(files)
            
            self.window.show()
            self.window.updateScreen(file_info, True)
            
            for result in results: 
                file_info += result+"\n\n"
        
            self.window.updateScreen(file_info, True)
        
        # Update the files on the screen for the user
        self.fetchServerFiles()
        self.fillTable()


    """ Uploads the files selected from the user to the server """
    def uploadFiles(self, files):
        results = list()
        self.ui.stackedWidget.setEnabled(False)
        try:
            for file in files:
                send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.UPLOAD_FILE.encode())
                
                #response = self.c_socket.recv(MAX_SIZE)
                response = recieve_data(self.c_socket)
                if response.decode() != ResponseCode.READY:
                    results.append(file + ": Error")
                    continue
                # Send the requested filepath to download the file at on 
                # the server's side
                path = self.currentServerPath() + os.path.basename(file)
        
                send_data(self.c_socket, self.S_PUBLIC_KEY, path.encode())
                
                # Check for duplicate
                #response = self.c_socket.recv(MAX_SIZE)
                response = recieve_data(self.c_socket)
                if response.decode() == ResponseCode.DUPLICATE:
                    results.append(file + ": Error, duplicate!")
                    continue;
                
                filesize = os.path.getsize(file)

                

                #self.c_socket.sendall(struct.pack("<Q", filesize))

                #with open(file, "rb") as f:
                #    while read_bytes := f.read(1024):
                #        self.c_socket.sendall(read_bytes)
                
                file_contents = bytes()
                with open(file, "rb") as f:
                    while read_bytes := f.read(1024):
                        file_contents += read_bytes
         
                send_data(self.c_socket, self.S_PUBLIC_KEY, file_contents)

                #response = self.c_socket.recv(MAX_SIZE)
                response = recieve_data(self.c_socket)
                response = response.decode()
                if response == ResponseCode.SUCCESS:
                    results.append(file + ": Success!")
                    # do something
                else:
                    results.append(file + ": Failure")
                    # do something

        except IOError:
            print("ERROR in uploadFiles!")
            return results

        return results


    """ Lets the user know they are attempting to delete a directory """
    def directory_delete_confirmation(self, selection):
        if selection.text() == "OK":
            self.deleteFileOrDirectory()


    """ 
        Checks whether the user is deleting a file or directory 
        and calls the corresponding function 
    """
    def deleteFile(self):
        
        # If multiple files are selected, delete them all
        if len(self.current_selection_list) != 0:
            self.currentSelectionListProcess(self.deleteFile)
            return
        
        directory = False
        directory_confirmation = False 
        if self.current_selection == None:
            print("None Error") # TODO show screen
            return

        with fileMutex:
            for file in self.files:
                if file.directory_flag == True and file.name == self.current_selection: 
                    directory = True
                    break
        
        # If its a directory, confirm deletion
        if directory:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText("This is a directory, are you sure you want to delete it?")
            msg.setWindowTitle("Directory Selected!")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.buttonClicked.connect(self.directory_delete_confirmation)
            msg.exec()
            return
        
        self.deleteFileOrDirectory() 


    """ Deletes a file from the server """
    def deleteFileOrDirectory(self):
        send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.DELETE_FILE.encode())
        
        #response = self.c_socket.recv(MAX_SIZE)
        response = recieve_data(self.c_socket)
       
        if response.decode() != ResponseCode.READY:
            return

        path = self.currentServerPath() + self.current_selection
        
        send_data(self.c_socket, self.S_PUBLIC_KEY, path.encode())

        #response = self.c_socket.recv(MAX_SIZE)
        response = recieve_data(self.c_socket)
        response = response.decode()
       
        # Show the user if the delete was successful or not
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Status")
        if response == ResponseCode.SUCCESS:
            msg.setText("Deletion Successfull!")
            msg.exec()
        elif response == ResponseCode.EDITING:
            msg.setText("There is someone currently editing this file, please wait " +
                        "and try again.")
            msg.exec()
        else:
            msg.setText("Error: file or directory could not be deleted, or " + 
                        "has already been deleted by another user.\nPlease " +
                        "refresh and try again.")
            msg.exec()
        
        self.refreshFiles()            


    """ Confirms if the user would like to download a directory """
    def download_directory_confirmation(self, selection):
        if selection.text() == "OK":
            self.downloadDirectory()


    """ 
        Handles downloading a directory, and gives the user the status 
        of the download when it is done
    """
    def downloadDirectory(self):
        # I believe this should work for MAC, but untested.
        default_dir = os.path.expanduser("~/Documents")
        
        # Dialog for the user to select a directory. Here they
        # Should probably create a new directory to avoid errors.
        user_dir_path = QFileDialog().getExistingDirectory(
                                        self,  
                                        "Save Directory", 
                                        default_dir,
                                        QFileDialog.ShowDirsOnly
                                        )

        # No directory selected, user exited the file dialog 
        if user_dir_path == "":
            return
        
        # Status window for when we are done dowloading
        self.window = StatusWindow()
        self.window.setEnableWindow(self) 
        self.window.downloadWindow()
        
        selected_dir = self.current_selection

        server_path = self.currentServerPath() + selected_dir
        
        file_info = self.downloadNestedDirectories(selected_dir, user_dir_path, server_path)
        
        # Show the download status of the files
        self.window.show()
        self.window.updateScreen(file_info, True)

    
    """
        This function is the core for downloading directories. It is a recursive function
        that will create a new folder for any nested directories and download all the files 
        each specified directory. It goes all the way down to the leaves of the file directory tree. 
    """
    def downloadNestedDirectories(self, directory, user_dir_path, server_path):
        dir_files = list()
        nested_dirs = list()
        
        # fileMutex is locked from downloadFile 
        # (call stack should look like downloadFile, 
        #                              download_directory_confirmation, 
        #                              downloadDirectory, 
        #                              downloadNestedDirectories)
        for file in self.files:
            if file.current_dir == directory:
                if file.directory_flag == True:
                    nested_dirs.append(file)
                else:
                    dir_files.append(file)
            
        file_info = ""
        
        # Iterates through all of the current directories files and requests to download them.
        for file in dir_files: 
            file_path = user_dir_path + "/" + file.name        
            selected_file = server_path + "/" + file.name
            
            send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.DOWNLOAD_FILE.encode())

            #response = self.c_socket.recv(MAX_SIZE)
            response = recieve_data(self.c_socket)
            
            if response.decode() != ResponseCode.READY:
                file_info += selected_file + ": Server Error.\n\n"
                continue

            status = self.downloadFileFromServer(selected_file, file_path)
            
            if status == ResponseCode.EDITING:
                file_info += selected_file + ": Error, someone currently editing.\n\n"
                continue

            elif status != ResponseCode.SUCCESS:
                file_info += selected_file + ": Error.\n\n"
                continue
        
            file_info += selected_file + ": Success!\n\n"
        
        # Recursively calls this function again if any subdirectories were found.
        for n_dir in nested_dirs: 
            new_server_path = server_path + "/" + n_dir.name
            new_user_path = user_dir_path + "/" + n_dir.name
            
            try:
                os.mkdir(new_user_path)
                file_info += new_user_path + ": Created directory!\n\n"
            except OSError as error:
                if error is FileExistsError:
                    file_info += new_user_path + ": Directory already exists!\n\n"
                else:
                    file_info += new_user_path + ": Error creating directory!\n\n"
                continue
            
            info = self.downloadNestedDirectories(n_dir.name, new_user_path, new_server_path) 
            
            if info != None and info != "": 
                file_info += info
        
        return file_info


    """ Downloads a file from the server """ 
    def downloadFile(self):
        
        # If multiple files are selected, download them all
        if len(self.current_selection_list) != 0:
            self.currentSelectionListProcess(self.downloadFile)
            return

        with fileMutex:
            files = list()
            directory = False

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowTitle("Status")

            if self.current_selection is None:
                msg.setText("Please select a file to download!")
                msg.exec()
                return
            
            for file in self.files:
                if file.directory_flag == True and file.name == self.current_selection: 
                    directory = True
                    break
           
            # Start of downloading a directory. 
            if directory:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                msg.setText("This is a directory, are you sure you want to download all " + 
                            "the files?\n\nNote: This process will overwrite any existing files " +
                            "with the same name in the directory you select, so it is advised to " +
                            "create a new directory for the download process.")
                msg.setWindowTitle("Directory Selected!")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.buttonClicked.connect(self.download_directory_confirmation)
                msg.exec()
                return

            send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.DOWNLOAD_FILE.encode())

            #response = self.c_socket.recv(MAX_SIZE)
            response = recieve_data(self.c_socket)
            
            if response.decode() != ResponseCode.READY:
                msg.setText("There was an error on the server's side, " +
                            "Please refresh and try again!")
                msg.exec()
                return 

            # I believe this should work for MAC, but untested.
            default_dir = os.path.expanduser("~/Documents" + "/" + self.current_selection)
            
            filename = QFileDialog().getSaveFileName(self, "Save File", default_dir) 
            
            selected_file = self.currentServerPath() + self.current_selection
            
            if filename[0] == "":
                send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.ERROR.encode())
                return
            
            status = self.downloadFileFromServer(selected_file, filename[0])
            
            if status == ResponseCode.EDITING:
                msg.setText("There is someone currently editing this file, please wait " +
                            "and try again.")
                msg.exec()
                return

            elif status != ResponseCode.SUCCESS:
                msg.setText("There was an error on the server's side, " +
                        "Please refresh and try again!")
                msg.exec()
                return

            return


    """
        A user has the option to download whole directories, so this takes care of 
        downloading a singular file. 
    """
    def downloadFileFromServer(self, selected_file, file):
        send_data(self.c_socket, self.S_PUBLIC_KEY, selected_file.encode())
            
        #response = self.c_socket.recv(MAX_SIZE)
        response = recieve_data(self.c_socket)
        
        if response.decode() != ResponseCode.SUCCESS:
            return response.decode()
       
        # Let the server know we are ready to get the file
        send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.READY.encode())

        self.recieveFile(file)

        return ResponseCode.SUCCESS


    """ Edits a file from the server """ 
    def editFile(self):
        directory = False
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Status")
        
        # If multiple files are selected, error
        if len(self.current_selection_list) != 0:
            msg.setText("Error: Please select a single file.")
            msg.exec()
            return
       
        # Case for no file selected
        if self.current_selection is None:
            msg.setText("Error: Please select a file to edit.")
            msg.exec()
            return 
        
        with fileMutex:
            for file in self.files:
                if file.directory_flag == True and file.name == self.current_selection: 
                    directory = True
                    break

        if directory:
            msg.setText("Error: Directory selected")
            msg.exec()
            return
        
        # Show the edit screen
        self.ui.stackedWidget.setCurrentIndex(EDIT_SCREEN)
        
        # Clear out any previous file that was edited
        self.ui.file_contents_area.clear()
        
        self.EDITING = True

        edit_file = self.currentServerPath() + self.current_selection  
        
        send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.EDIT_FILE.encode())
        
        #response = self.c_socket.recv(MAX_SIZE)
        response = recieve_data(self.c_socket)
        
        if response.decode() != ResponseCode.READY:
            self.ui.stackedWidget.setCurrentIndex(MAIN_SCREEN)
            msg.setText("There was an error on the server's side, " +
                        "Please refresh and try again!")
            msg.exec()
            self.EDITING = False
            return


        send_data(self.c_socket, self.S_PUBLIC_KEY, edit_file.encode())
        
        #response = self.c_socket.recv(MAX_SIZE)
        response = recieve_data(self.c_socket)
        
        if response.decode() == ResponseCode.DUPLICATE:
            self.ui.stackedWidget.setCurrentIndex(MAIN_SCREEN)
            msg.setText("There is someone currently editing this file, please wait " +
                        "and try again.")
            msg.exec() 
            self.EDITING = False
            return
        
        elif response.decode() == ResponseCode.ERROR:
            self.ui.stackedWidget.setCurrentIndex(MAIN_SCREEN)
            msg.setText("There was an error on the server's side, " +
                        "Please refresh and try again!")
            msg.exec()
            self.EDITING = False
            return
        
        elif response.decode() != ResponseCode.SUCCESS:
            self.ui.stackedWidget.setCurrentIndex(MAIN_SCREEN)
            msg.setText("There was an error on the server's side, " +
                        "Please refresh and try again!")
            msg.exec()
            self.EDITING = False
            return
       
        # If we refresh the file list while downloading the file that is being edited, there may be an error
        with fileMutex:  
            send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.READY.encode())
            
            # Create a temporary file so we can download the file using 
            # previously defined methods.
            tmp = tempfile.NamedTemporaryFile(delete = False)
            try:
                self.recieveFile(tmp.name)
                tmp.seek(0)
                self.ui.edit_file_name.setText(edit_file)
                file = tmp.read().decode()
                self.ui.file_contents_area.insertPlainText(file)

            # Just in case the server accidentally sends us a binary file
            except UnicodeDecodeError:
                self.editCancel()
            
            finally:
                tmp.close()
                try:
                    os.unlink(tmp.name)
                except Exception:
                    pass


    """ Saves the file requested to be edited from the server (reuploads it) """ 
    def editSave(self):
        self.EDITING = False
        
        send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.READY.encode())

        response = recieve_data(self.c_socket)
        print("Letting the server know that we are ready", flush = True)
        if response.decode() != ResponseCode.READY:
            return

        text = self.ui.file_contents_area.toPlainText()
        
        file = text.encode()

        #self.c_socket.sendall(struct.pack("<Q", len(file)))
        #self.c_socket.sendall(file)
        send_data(self.c_socket, self.S_PUBLIC_KEY, file)

        self.ui.file_contents_area.clear()

        self.ui.stackedWidget.setCurrentIndex(MAIN_SCREEN)

        self.refreshFiles()


    """ Cancels an edit request for a server file """ 
    def editCancel(self):
        self.EDITING = False
        
        send_data(self.c_socket, self.S_PUBLIC_KEY, ResponseCode.ERROR.encode())
        self.ui.file_contents_area.clear()
        self.ui.stackedWidget.setCurrentIndex(MAIN_SCREEN)
    
        self.refreshFiles()


# Start of the program :) ... just some PySide6 stuff to get the window opened.
app = QApplication([])

window = Window()
window.show()

app.exec()
