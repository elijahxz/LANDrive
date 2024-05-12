from enum import StrEnum
"""
READ ME!!!!!!
This file is shared between the client.py and server.py. 
If you make changes to it, make sure to update the shared.py 
that is in the same directory as client.py AND server.py 
(Usually, they are not in the same directory, so BE CAREFUL)
"""

MAX_SIZE = 1024

# Used on the server side to specify which directory to look in (needs \)
# If you change this variable, there must be a matching file directory where server.py is located.
SERVER_ROOT_DIR = "\\FileDirectory"

# Used in client side to specify root directory of server (doesn't need \)
BASE_DIR = SERVER_ROOT_DIR[1:]


""" 
    Commands that can be requested from the client
    They are in a module because match/case statements
    semantics are not the same if variables are used
"""
class ResponseCode(StrEnum):
    CLOSE_CONNECTION = "TerminateTCPConnection"
    REFRESH          = "RefreshFiles"
    USERS            = "GetTCPUsers"
    CREATE_DIR       = "CreateDirectory"
    UPLOAD_FILE      = "TCPUploadFile"
    DOWNLOAD_FILE    = "TCPDownloadFile"
    EDIT_FILE        = "TCPEditFile"
    DELETE_FILE      = "DeleteFile"
    DUPLICATE        = "Duplicate"
    SUCCESS          = "Success"
    ERROR            = "Error"
    EDITING          = "FileInUse"
    READY            = "Ready"

# This class is what gets sent to the client from the server
# When the client requests for a refresh. 
class FileInfo:
    def __init__(self):
        self.rel_path = ""
        self.name = ""
        self.current_dir = ""
        self.time_stamp = ""
        self.size = ""
        self.directory_flag = False
    
    def update(self, rel_path, name, current_dir, time_stamp, size, directory_flag = False):
        self.rel_path = rel_path
        self.name = name
        self.current_dir = current_dir 
        self.time_stamp = time_stamp 
        self.size = size
        self.directory_flag = directory_flag
        return 
