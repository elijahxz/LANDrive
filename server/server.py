import json
import os
import pickle
import signal
import shutil
import socket
import struct
import sys
import threading
import time
from pathlib import Path
from shared import *
from enum import StrEnum
 
""" 
    To run on a LAN, change the HOST variable to your
    IPv4 IP address that will host the server. 
"""
HOST = "127.0.0.1"

"""
    If you run into an error starting the server, you 
    can try changing the port. 
"""
PORT = 8504

""" Max users for the server """
MAX_USERS = 16

SERVER_FILES = list()
DIRECTORIES = list()

EDIT_STACK = list()

SERVER_TERMINATE = False

USER_COUNT = 0

PRIVATE_KEY = None
PUBLIC_KEY = None

user_mutex = threading.Lock()
edit_mutex = threading.Lock()
refresh_mutex = threading.Lock()
upload_mutex = threading.Lock()
delete_mutex = threading.Lock()

def main():
    global SERVER_TERMINATE
    global USER_COUNT
    global PRIVATE_KEY
    global PUBLIC_KEY
    PUBLIC_KEY, PRIVATE_KEY = generate_rsa_keys()

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
           
            with user_mutex:
                USER_COUNT += 1
            
            # Create a new thread to handle the client
            # This thread runs the client_handler function
            client_thread = threading.Thread(target=client_handler, args=(c_socket,))
            client_thread.start()
    
    # When Ctrl + C, show that the server is closing
    # TODO This does not work for some reason?
    except KeyboardInterrupt:
        stdoutPrint("Server shutting down...")
        
        SERVER_TERMINATE = True
        file_thread.join()

        s_socket.close()
        sys.exit()

    return


""" 
    I may be using threads and sockets wrong, because printing will 
    not work unless I flush stdout after each print statement
"""
def stdoutPrint(message):
    print(message)
    sys.stdout.flush()

""" Function to handle client connections """
def client_handler(c_socket):
    global USER_COUNT
    try:
        files = list()
        
        # Get the client's public key and send out server public key
        stdoutPrint("Sending Public Key")
        send_key(c_socket, PUBLIC_KEY)
        
        stdoutPrint("Recieving Public Key")
        c_public_key = recieve_key(c_socket)
       
        #data = recieve_data(c_socket)
        send_data(c_socket, c_public_key, pickle.dumps(SERVER_FILES)) 
        
        #send_data(c_socket, c_public_key, ResponseCode.SUCCESS.encode())
        
        data = recieve_data(c_socket)
        
        if data.decode() != ResponseCode.SUCCESS: 
            stdoutPrint("Error: Public Key Exchange Failed")
            return
        else:
            stdoutPrint("Success: Public Key Exchange Completed")

        while True:
            # recieve data from the client
            #request = c_socket.recv(MAX_SIZE)
            stdoutPrint("Recieving Data From Client")
            request = recieve_data(c_socket)
            stdoutPrint("Recieved data!")
            
            buffer = request.decode()
            stdoutPrint(buffer)
            
            match buffer:
                # This breaks the while loop!
                case ResponseCode.CLOSE_CONNECTION:
                    with user_mutex:
                        USER_COUNT -= 1
                    break

                case ResponseCode.USERS:
                    with user_mutex:
                        send_data(c_socket, c_public_key, str(USER_COUNT).encode())

                # Send the files in the server's directory to the user
                case ResponseCode.REFRESH:
                    with refresh_mutex:
                        sent = 0
                        data = pickle.dumps(SERVER_FILES)
                        
                        send_data(c_socket, c_public_key, data)

                        #stream = bytes(data)
                        #stream_length = len(stream)
                        #c_socket.sendall(struct.pack("<Q", stream_length))
                        #c_socket.sendall(stream)

                case ResponseCode.UPLOAD_FILE:
                    with upload_mutex:
                        upload_file_to_server(c_socket, c_public_key)

                case ResponseCode.DOWNLOAD_FILE:
                    # A person can not delete a file that is trying to be dowloaded
                    with delete_mutex:
                        download_file(c_socket, c_public_key)
                
                case ResponseCode.EDIT_FILE:
                    edit_file(c_socket, c_public_key)

                case ResponseCode.DELETE_FILE:
                    with delete_mutex:
                        delete_file(c_socket, c_public_key)
                
                case ResponseCode.CREATE_DIR:
                    with refresh_mutex:
                        create_directory(c_socket, c_public_key)

                case _:
                    stdoutPrint("An error has occured, %s is not a valid client request" 
                                % (buffer))
             
            stdoutPrint("Client message: %s" % (buffer))
            if (buffer == ResponseCode.CLOSE_CONNECTION):
                break
            
        # Close the connection with the client
        c_socket.close()

    except Exception:
        # Assume there was an error with the socket, so this thread will be interupted and end
        with user_mutex:
            USER_COUNT -= 1


"""
    Get an updated list of available files from the server
"""
def getServerFiles():
    global SERVER_FILES, DIRECTORIES
    while not SERVER_TERMINATE: 
        with refresh_mutex:
            file_list = list()
            dirs = list()
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
                    
                    dirs.append(subdir)

                    file_list.append(new_dir) 
            
            SERVER_FILES = file_list
            DIRECTORIES = dirs 
        # The corresponding thread will check and update the files 
        # Approx. every second (with mutex locking it may vary)
        time.sleep(1)


"""
    Gets the details of each file on the server.
    Note: Directory size is wrong usually
"""
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


""" 
    Handles the request to upload a file to the server.
"""
def upload_file_to_server(c_socket, c_public_key):
    done = False
    
    # Let the client know we are ready
    send_data(c_socket, c_public_key, ResponseCode.READY.encode())

    #file_path = c_socket.recv(MAX_SIZE)
    file_path = recieve_data(c_socket)
    file_path = file_path.decode() 

    server_py_path = os.path.dirname(os.path.realpath(__file__)) 
    
    directory_path = server_py_path + "/" + file_path

    print(directory_path)
    
    basename = os.path.basename(directory_path)
    
    try:
        file = open(directory_path, "rb")
        send_data(c_socket, c_public_key, ResponseCode.DUPLICATE.encode())
        return
    except IOError:
        file = open(directory_path, "wb")
        send_data(c_socket, c_public_key, ResponseCode.SUCCESS.encode())
    
    stdoutPrint(directory_path)
    
    recieve_file(c_socket, directory_path)
    
    send_data(c_socket, c_public_key, ResponseCode.SUCCESS.encode())


"""
    Since files can be larger than MAX_SIZE, we have to create a struct and 
    send over the file size, then the file directly after
"""
def recieve_file_size(c_socket):
    fmt = "<Q"
    expected_bytes = struct.calcsize(fmt)
    recieved_bytes = 0
    stream = bytes()

    while recieved_bytes < expected_bytes:
        chunk = c_socket.recv(expected_bytes - recieved_bytes)
        stream += chunk
        recieved_bytes += len(chunk)
    filesize = struct.unpack(fmt, stream)[0]
    return filesize


"""
    Recieves the file information from the client
"""
def recieve_file(c_socket, filename):
    # First read from the socket the amount of
    # bytes that will be recieved from the file.
    #filesize = recieve_file_size(c_socket)
    
    file = recieve_data(c_socket)
    
    # Open a new file where to store the recieved data.
    with open(filename, "wb") as f:
        #recieved_bytes = 0
        # recieve the file data in 1024-bytes chunks
        # until reaching the total amount of bytes
        # that was informed by the client.
        #while recieved_bytes < filesize:
        #    chunk = c_socket.recv(MAX_SIZE)
        #    if chunk:
        #        recieved_bytes += len(chunk)
        f.write(file)


"""
    Creates a directory on the server's side
"""
def create_directory(c_socket, c_public_key):
    send_data(c_socket, c_public_key, ResponseCode.READY.encode())
    
    #path = c_socket.recv(MAX_SIZE)
    path = recieve_data(c_socket)
    server_py_path = os.path.dirname(os.path.realpath(__file__)) 
    directory_path = Path(server_py_path + "/" + path.decode())
    
    create_dir = os.path.basename(directory_path)
    if create_dir in DIRECTORIES:
        send_data(c_socket, c_public_key, ResponseCode.ERROR.encode())
        return

    try:
        os.mkdir(directory_path)
        send_data(c_socket, c_public_key, ResponseCode.SUCCESS.encode()) 
    except OSError as error:
        if error is FileExistsError:
            send_data(c_socket, c_public_key, ResponseCode.DUPLICATE.encode())
        else:
            send_data(c_socket, c_public_key, ResponseCode.ERROR.encode())
        return


""" 
    Deletes a file (or directory) on the server's side
"""
def delete_file(c_socket, c_public_key):
    send_data(c_socket, c_public_key, ResponseCode.READY.encode())
    
    #file_path = c_socket.recv(MAX_SIZE)
    file_path = recieve_data(c_socket)
    file_path = file_path.decode() 
    
    server_py_path = os.path.dirname(os.path.realpath(__file__)) 
        
    directory_path = Path(server_py_path + "/" + file_path)
   
    if check_edit_stack( (server_py_path + "/" + file_path) ):
        send_data(c_socket, c_public_key, ResponseCode.EDITING.encode())
        return
    
    # Directory case
    if os.path.isdir(directory_path):
        shutil.rmtree(directory_path)
        send_data(c_socket, c_public_key, ResponseCode.SUCCESS.encode())
    
    # File case
    elif os.path.isfile(directory_path):
        os.remove(directory_path)
        send_data(c_socket, c_public_key, ResponseCode.SUCCESS.encode())
   
    # DNE case (probably already deleted and user did not refresh)
    else:
        send_data(c_socket, c_public_key, ResponseCode.ERROR.encode())


"""
    Sends file data from the client to the server
"""
def download_file(c_socket, c_public_key):
    send_data(c_socket, c_public_key, ResponseCode.READY.encode())

    #file = c_socket.recv(MAX_SIZE)
    file = recieve_data(c_socket)
    file = file.decode()
    
    # This means the user clicked cancel when selecting a file to save to.
    if file == ResponseCode.ERROR:
        return

    server_py_path = os.path.dirname(os.path.realpath(__file__)) 
    
    path = server_py_path + "/" + file
    
    if check_edit_stack(path):
        send_data(c_socket, c_public_key, ResponseCode.EDITING.encode())
        return
    
    # Ensure the file has not been deleted already
    try:
        f = open(path, "rb")
    except FileNotFoundError:
        send_data(c_socket, c_public_key, ResponseCode.ERROR.encode())
        return 
   
    send_data(c_socket, c_public_key, ResponseCode.SUCCESS.encode())
    
    #response = c_socket.recv(MAX_SIZE)
    response = recieve_data(c_socket)
    
    if response.decode() != ResponseCode.READY:
        return

    

    #c_socket.sendall(struct.pack("<Q", os.path.getsize(path)))
    #while read_bytes := f.read(MAX_SIZE):
    #    c_socket.sendall(read_bytes)

    file_contents = bytes()
    while read_bytes := f.read(MAX_SIZE):
        file_contents += read_bytes

    send_data(c_socket, c_public_key, file_contents)

def check_edit_stack(entry):
    with edit_mutex:
        for file in EDIT_STACK:
            if file == entry:
                return True
    
    return False


def add_to_edit_stack(entry):
    global EDIT_STACK
    with edit_mutex:
        EDIT_STACK.append(entry)


def remove_from_edit_stack(entry):
    global EDIT_STACK
    counter = 0
    with edit_mutex:
        for file in EDIT_STACK:
            if file == entry:
                del EDIT_STACK[counter]
                return
            counter += 1

""" Sends a file to the client to edit, then waits for the client to exit or send back the file """
def edit_file(c_socket, c_public_key):
    try:
        send_data(c_socket, c_public_key, ResponseCode.READY.encode())
        
        #response = c_socket.recv(MAX_SIZE)
        response = recieve_data(c_socket)
        file_name = response.decode()
        

        server_py_path = os.path.dirname(os.path.realpath(__file__)) 
           
        # We want the string version to add to the edit stack
        file_path = server_py_path + "/" + file_name

        if check_edit_stack(file_path):
            send_data(c_socket, c_public_key, ResponseCode.DUPLICATE.encode())
            return
        
        add_to_edit_stack(file_path)
        try:
            file = open(file_path, "rb")
            textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
            is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
            if is_binary_string(file.read(MAX_SIZE)):
                raise FileNotFoundError
        except Exception:
            send_data(c_socket, c_public_key, ResponseCode.ERROR.encode())
            remove_from_edit_stack(file_path)
            return 
        
        send_data(c_socket, c_public_key, ResponseCode.SUCCESS.encode())
        
        #response = c_socket.recv(MAX_SIZE)
        response = recieve_data(c_socket)
        
        if response.decode() != ResponseCode.READY:
            remove_from_edit_stack(file_path)
            return
        
        file = open(file_path, "rb")
        
        file_contents = bytes()
        while read_bytes := file.read(MAX_SIZE):
            file_contents += read_bytes

        send_data(c_socket, c_public_key, file_contents)

       # c_socket.sendall(struct.pack("<Q", os.path.getsize(file_path)))
       # while read_bytes := file.read(MAX_SIZE):
       #     c_socket.sendall(read_bytes)
        file.close()

        #response = c_socket.recv(MAX_SIZE)
        response = recieve_data(c_socket)
        
        # This means the user backed out from editing the file
        if response.decode() != ResponseCode.READY:
            stdoutPrint("Client not ready, so remove file")
            remove_from_edit_stack(file_path)
            return
       
        send_data(c_socket, c_public_key, ResponseCode.READY.encode())

        stdoutPrint("Attempting to recievefile")
        recieve_file(c_socket, file_path)

        remove_from_edit_stack(file_path)
    except Exception as e:
        stdoutPrint(e)

# Start program by calling main()
if __name__ == "__main__":
    main()
