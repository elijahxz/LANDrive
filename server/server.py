import json
import os
import socket
import sys
import time
import threading
import pickle
from shared import HOST, PORT, SERVER_ROOT_DIR, MAX_SIZE, ResponseCode, FileInfo
from enum import StrEnum

# This app does not ask the client to insert a port,
# so the server and client always tries to access
# 8504 on localhost
MAX_USERS = 16
# Random max size, may increase if needed
SERVER_FILES = list()

SERVER_TERMINATE = False

mutex = threading.Lock()

def main():
    global SERVER_TERMINATE

    stdoutPrint("Server running...\n")
    # TCP socket
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    s_socket.bind((HOST, PORT))

    # Allow up to 16 users at once
    s_socket.listen(MAX_USERS)
    
    stdoutPrint("Server now listening on %s:%d\n" % (HOST, PORT))
   
    file_thread = threading.Thread(target=getServerFiles)
    file_thread.start()

    try:
        while True:
            # Accept incoming connections from clients
            c_socket, c_address = s_socket.accept()
            stdoutPrint("Client connected, client's address = %s" % (c_address,))
            sys.stdout.flush()
            
            # Create a new thread to handle the client
            # This thread runs the client_handler function
            client_thread = threading.Thread(target=client_handler, args=(c_socket,))
            client_thread.start()
    # When Ctrl + C, show that the server is closing
    except KeyboardInterrupt:
        stdoutPrint("Server shutting down...")
        
        SERVER_TERMINATE = True
        file_thread.join()

        s_socket.close()
        sys.exit()
    
    return

# I may be using threads and sockets wrong, because printing 
# will not work unless I flush stdout after each print statement
def stdoutPrint(message):
    print(message)
    sys.stdout.flush()

# Function to handle client connections
def client_handler(c_socket):
    files = list()

    while True:
        # Receive data from the client
        request = c_socket.recv(MAX_SIZE)
        
        buffer = request.decode()
        
        match buffer:
            case ResponseCode.CLOSE_CONNECTION:
                break # This breaks the while loop!
            # Send the files in the server's directory to the user
            case ResponseCode.REFRESH:
                with mutex:
                    data = pickle.dumps(SERVER_FILES)
                    c_socket.sendall(bytes(data))
            case _:
                stdoutPrint("An error has occured, %s is not a valid client request" 
                            % (buffer))
         
        stdoutPrint("Client message: %s" % (buffer))
        if (buffer == ResponseCode.CLOSE_CONNECTION):
            break
        
    # Close the connection with the client
    c_socket.close()

"""
    Get an updated list of available files from the server
    Output structure:
        A list of lists, each sublist looks like this:
            [relative path, file name]
"""
def getServerFiles():
    global SERVER_FILES
    file_list = list()
    
    while not SERVER_TERMINATE: 
        with mutex:
            file_list = list()
            # Gets the path of this file, server.py. 
            # FileDirectory/ should be at the same path 
            server_py_path = os.path.dirname(os.path.realpath(__file__)) 
            file_directory_path = server_py_path + SERVER_ROOT_DIR
            
            # Get all of the files unser FileDirectory\
            for path, subdirs, files in os.walk(file_directory_path):
                rel_path = path[path.find(SERVER_ROOT_DIR):]
                current_dir = os.path.basename(rel_path)
                for name in files:
                    t_stamp, size = process_file_information(os.path.join(path,name))
                    relative_path = os.path.join(rel_path, name) 
                    
                    new_file = FileInfo()
                    new_file.update(rel_path, name, current_dir, t_stamp, size, False)

                    file_list.append(new_file)
                for subdir in subdirs: 
                    t_stamp, size = process_file_information(os.path.join(path,subdir), True)
                    # Size information for directories seems to be wrong, so just specify that its a directory
                    size = "Directory" 
                    relative_path = os.path.join(rel_path, subdir) 
                    
                    new_dir = FileInfo()
                    new_dir.update(relative_path, subdir, current_dir, t_stamp, size, True)
                    
                    file_list.append(new_dir) 
            
            SERVER_FILES = file_list
   
        # The corresponding thread will check and update the files 
        # Approx. every 10 seconds
        time.sleep(10)
def process_file_information(file_path, directory = False):
    kilobytes = 1024.00
    megabytes = kilobytes * 1024.00
    gigabytes = megabytes * 1024.00
    size = "" 

    # Timestamp
    modify_time = os.path.getmtime(file_path) 
    t_ctime = time.ctime(modify_time)
    time_obj = time.strptime(t_ctime)
    t_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time_obj)
    
    file_size = os.stat(file_path).st_size
    if (file_size >= gigabytes):
        file_size /= gigabytes 
        size = "{:.2f} Gb".format(file_size)
    elif file_size >= megabytes: 
        file_size /= megabytes
        size = "{:.2f} Mb".format(file_size)
    elif file_size >= kilobytes:
        file_size /= kilobytes 
        size = "{:.2f} Kb".format(file_size)
    else: 
        size = "{:.0f} Bytes".format(file_size)

    return t_stamp, size

# Start program by calling main()
if __name__ == "__main__":
    main()
