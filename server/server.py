import os
import socket
import sys
import threading

# This app does not ask the client to insert a port,
# so the server and client always tries to access
# 8504 on localhost
HOST = "127.0.0.1"
PORT = 8504
MAX_USERS = 16
# Random max size, may increase if needed
MAX_SIZE = 16384
CLOSE_CONNECTION = "TerminateTCPConnection"
PRINT_LOCK = threading.Lock()

# Function to handle client connections
def client_handler(c_socket):
    
    while True:
        # Receive data from the client
        request = c_socket.recv(MAX_SIZE)
        
        buffer = request.decode()
        
        stdoutPrint("Client message: %s" % (buffer))
        if (buffer == CLOSE_CONNECTION):
            PRINT_LOCK.release()
            break

        # Send a response back to the client
        response = "Hello from the server!"
        c_socket.send(response.encode())
        
    # Close the connection with the client
    c_socket.close()


def main():
    stdoutPrint("Server running...\n")

    # TCP socket
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    s_socket.bind((HOST, PORT))

    # Allow up to 16 users at once
    s_socket.listen(MAX_USERS)
    
    stdoutPrint("Server now listening on %s: %d\n" % (HOST, PORT))

    try:
        while True:
            # Accept incoming connections from clients
            c_socket, c_address = s_socket.accept()
            stdoutPrint("Client connected, client's address = %s" % (c_address,))
            sys.stdout.flush()
            
            PRINT_LOCK.acquire()
            # Create a new thread to handle the client
            # This thread runs the client_handler function
            client_thread = threading.Thread(target=client_handler, args=(c_socket,))
            client_thread.start()
    # When Ctrl + C, show that the server is closing
    except KeyboardInterrupt:
        stdoutPrint("Server shutting down...")
        s_socket.close()
        sys.exit()
    
    return

# I may be using threads and sockets wrong, because printing 
# will not work unless I flush stdout after each print statement
def stdoutPrint(message):
    print(message)
    sys.stdout.flush()



if __name__ == "__main__":
    main()
