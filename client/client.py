import os
import json
import time
import pickle
import socket
import struct
import sys
import tempfile
from datetime import datetime
from threading import Lock

from shared import HOST, PORT, BASE_DIR, MAX_SIZE, ResponseCode, FileInfo

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
    uploads files from their local machine
"""
class StatusWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.window = False
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.closeBtn.clicked.connect(self.closeCustomEvent)

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
"""
class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
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

        # Create a socket for the client
        self.c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Initialize the other class and set everything up
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setupUiFunctionality()

        # Setup the exit program & change theme option for the context menu
        self.context_menu = QMenu(self)
        action1 = self.context_menu.addAction("Change Theme")
        action1.triggered.connect(self.changeTheme)
        action2 = self.context_menu.addAction("Exit Program")
        action2.triggered.connect(QApplication.quit)
  
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

    """ Called when the GUI is closed """
    def closeEvent(self, event):
        event.accept()
        
        # If we are editing a file, let the server know we are done
        if self.EDITING:
            self.editCancel()

        # Always try to close the socket when the user closes the application
        try:
            self.c_socket.send(ResponseCode.CLOSE_CONNECTION.encode())
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

    """ If we try to disconnect while editing a file, let the server know """
    def disconnectFromServerWhileEditing(self):
        self.editCancel()
        self.disconnectFromServer()

    """ Disconnects from the server and shows the connect screen """
    def disconnectFromServer(self):
        self.c_socket.send(ResponseCode.CLOSE_CONNECTION.encode())
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
    
    """ 
        Called when a table element is clicked
        This is stored in a variable for future functionality
    """
    def currentSelection(self, element):
        self.current_selection = self.ui.tableWidget.item(element.row(), 0).text()
  
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

    """ Used to recieve a file, this gets the size of the file """
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

    """ Recieves data from the server (used in self.fetchServerFiles) """
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

    """ Recieves a file from the server and saves it to the specified filename """
    def recieveFile(self, filename):
        # First read from the socket the amount of
        # bytes that will be recieved from the file.
        filesize = self.recieveDataSize()
        # Open a new file where to store the recieved data.
        with open(filename, "wb") as f:
            recieved_bytes = 0
            # recieve the file data in 1024-bytes chunks
            # until reaching the total amount of bytes
            # that was informed by the client.
            while recieved_bytes < filesize:
                chunk = self.c_socket.recv(MAX_SIZE)
                if chunk:
                    recieved_bytes += len(chunk)
                    f.write(chunk)
    
    """ Gets the current version of the server files from the server """
    def fetchServerFiles(self):
        self.c_socket.send(ResponseCode.REFRESH.encode())
       
        data = self.recieveData()

        # We assume no error when pickling the file, but there 
        # should be a try/catch block here...TODO for the future
        with fileMutex:
            self.files = pickle.loads(data)
       
        now = datetime.now()

        #date_string = now.strftime("%B %d, %Y %H:%M:%S")
        date_string = now.strftime("%H:%M:%S")
        self.ui.updated.setText("Last Updated: " + date_string)
        self.ui.updated.repaint()

        self.c_socket.send(ResponseCode.USERS.encode())

        data = self.c_socket.recv(MAX_SIZE)
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
        with fileMutex:
            for file in self.files:
                if file.current_dir == self.dir_stack[ ( len(self.dir_stack) - 1 ) ]:
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
    
    
    def checkIfDirectoryExists(self, directory):
        self.refreshFiles()

        valid_selection = False
        with fileMutex:
            for file in self.files:
                if file.directory_flag == True and file.name == directory: 
                    valid_selection = True
                    break
        if directory == BASE_DIR: 
            valid_selection = True

        return valid_selection
    
    def goToValidDirectory(self):
        self.refreshFiles()

        valid = False
        while not valid:
            self.dir_stack.pop()
            dir_num = len(self.dir_stack) - 1
            
            if dir_num >= 0:
                valid = self.checkIfDirectoryExists(self.dir_stack[dir_num])
            # Base directory will always be valid
            else:
                valid = True

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

            self.c_socket.send(ResponseCode.CREATE_DIR.encode())
                
            response = self.c_socket.recv(MAX_SIZE)
            if response.decode() != ResponseCode.READY:
                msg.setText("There was an error on the server's side, " +
                            "Please refresh and try again!")
                msg.exec()
                return
            
            path = self.currentServerPath() + text

            self.c_socket.send(path.encode())
            
            response = self.c_socket.recv(MAX_SIZE)

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
                self.c_socket.send(ResponseCode.UPLOAD_FILE.encode())
                
                response = self.c_socket.recv(MAX_SIZE)
                if response.decode() != ResponseCode.READY:
                    results.append(file + ": Error")
                    continue
                # Send the requested filepath to download the file at on 
                # the server's side
                path = self.currentServerPath() + os.path.basename(file)
        
                self.c_socket.send(path.encode())
                
                # Check for duplicate
                response = self.c_socket.recv(MAX_SIZE)
                if response.decode() == ResponseCode.DUPLICATE:
                    print("Duplicate on serverside")
                    results.append(file + ": Error, duplicate!")
                    continue;
                
                filesize = os.path.getsize(file)
                self.c_socket.sendall(struct.pack("<Q", filesize))

                with open(file, "rb") as f:
                    while read_bytes := f.read(1024):
                        self.c_socket.sendall(read_bytes)


                response = self.c_socket.recv(MAX_SIZE)
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
        directory = False
        directory_confirmation = False 
        if self.current_selection == None:
            print("None Error") # TODO show screen
            return

        with fileMutex:
            for file in self.files:
                print(file.directory_flag, file.current_dir, self.current_selection)
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
        self.c_socket.send(ResponseCode.DELETE_FILE.encode())
        
        response = self.c_socket.recv(MAX_SIZE)
       
        if response.decode() != ResponseCode.READY:
            return

        path = self.currentServerPath() + self.current_selection
        
        self.c_socket.send(path.encode())

        response = self.c_socket.recv(MAX_SIZE)
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

    """ Downloads a file from the server """ 
    def downloadFile(self):
        files = list()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Status")

        if self.current_selection is None:
            msg.setText("Please select a file to download!")
            msg.exec()
            return
        
        self.c_socket.send(ResponseCode.DOWNLOAD_FILE.encode())

        response = self.c_socket.recv(MAX_SIZE)
        
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
            self.c_socket.send(ResponseCode.ERROR.encode())
            return

        self.c_socket.send(selected_file.encode())
        
        response = self.c_socket.recv(MAX_SIZE)
        
        if response.decode() == ResponseCode.EDITING:
            msg.setText("There is someone currently editing this file, please wait " +
                        "and try again.")
            msg.exec()
            return

        if response.decode() != ResponseCode.SUCCESS:
            msg.setText("There was an error on the server's side, " +
                        "Please refresh and try again!")
            msg.exec()
            return
       
        # Let the server know we are ready to get the file
        self.c_socket.send(ResponseCode.READY.encode())

        self.recieveFile(filename[0])


    """ Edits a file from the server """ 
    def editFile(self):
        directory = False
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("Status")
        
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
       
        self.ui.stackedWidget.setCurrentIndex(EDIT_SCREEN)
        
        self.EDITING = True

        edit_file = self.currentServerPath() + self.current_selection  
        
        self.c_socket.send(ResponseCode.EDIT_FILE.encode())
        
        response = self.c_socket.recv(MAX_SIZE)
        
        if response.decode() != ResponseCode.READY:
            self.ui.stackedWidget.setCurrentIndex(MAIN_SCREEN)
            msg.setText("There was an error on the server's side, " +
                        "Please refresh and try again!")
            msg.exec()
            self.EDITING = False
            return


        self.c_socket.send(edit_file.encode())
        
        response = self.c_socket.recv(MAX_SIZE)
        
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
        
        
        self.c_socket.send(ResponseCode.READY.encode())
        
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
        
        self.c_socket.send(ResponseCode.READY.encode())

        text = self.ui.file_contents_area.toPlainText()
        
        file = text.encode()

        self.c_socket.sendall(struct.pack("<Q", len(file)))
        self.c_socket.sendall(file)
        
        self.ui.file_contents_area.clear()

        self.ui.stackedWidget.setCurrentIndex(MAIN_SCREEN)

        self.refreshFiles()


    """ Cancels an edit request for a server file """ 
    def editCancel(self):
        self.EDITING = False
        
        self.c_socket.send(ResponseCode.ERROR.encode())
        self.ui.file_contents_area.clear()
        self.ui.stackedWidget.setCurrentIndex(MAIN_SCREEN)
    
        self.refreshFiles()




app = QApplication([])

window = Window()
window.show()

app.exec()
