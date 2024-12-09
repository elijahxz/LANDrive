import ast
import os
import pickle
import struct

from enum import StrEnum
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

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

PUBLIC_PATH = "reciever.pem"
PRIVATE_PATH = "private.pem" 

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
    PUBKEY           = "PublicKey"

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

def generate_rsa_keys():
    if os.path.exists(PUBLIC_PATH) and os.path.exists(PRIVATE_PATH):
        private_key = RSA.import_key(open(PRIVATE_PATH).read())
        public_key = RSA.import_key(open(PUBLIC_PATH).read())
        return public_key, private_key

    key = RSA.generate(2048)
    private_key = key.export_key()
    with open(PRIVATE_PATH, "wb") as f:
        f.write(private_key)

    public_key = key.publickey().export_key()
    with open(PUBLIC_PATH, "wb") as f:
        f.write(public_key)

    return public_key, private_key

""" Used to recieve a file, this gets the struct that is sent before the actual file """
def recieve_data_size(socket):
    fmt = "<Q"
    expected_bytes = struct.calcsize(fmt)
    recieved_bytes = 0
    stream = bytes()

    while recieved_bytes < expected_bytes:
        chunk = socket.recv(expected_bytes - recieved_bytes)
        stream += chunk
        recieved_bytes += len(chunk)
    
    datasize = struct.unpack(fmt, stream)[0]
    return datasize


""" 
    Recieves data from the server 
    Similar to recieveFile.
"""
def recieve_data(socket):
    # First read from the socket the amount of
    # bytes that will be recieved from the server.
    datasize = recieve_data_size(socket)

    recieved_bytes = 0
    data = bytes()
    # recieve the data in 1024-bytes chunks
    # until reaching the total amount of bytes
    # that was informed by the server.
    while recieved_bytes < datasize:
        chunk = socket.recv(MAX_SIZE)
        if chunk:
            recieved_bytes += len(chunk)
            data = data + chunk
    try:
        e_data = pickle.loads(data)
        decrypted_data = decrypt_data(e_data[0], e_data[1], e_data[2], e_data[3])
    except Exception as e:
        print("ERROR")
        return ""

    return decrypted_data

def recieve_key(socket):
    datasize = recieve_data_size(socket)
    recieved_bytes = 0
    data = bytes()
    # recieve the data in 1024-bytes chunks
    # until reaching the total amount of bytes
    # that was informed by the server.
    while recieved_bytes < datasize:
        chunk = socket.recv(MAX_SIZE)
        if chunk:
            recieved_bytes += len(chunk)
            data = data + chunk
    
    key = RSA.importKey(data)

    return key

def send_key(socket, key):
    binPubKey = key.publickey().exportKey('DER')
    stream = binPubKey
    stream_length = len(stream)
    socket.sendall(struct.pack("<Q", stream_length))
    socket.sendall(stream)
    return

def send_data(socket, key, data):
    enc_session_key, nonce, tag, ciphertext = encrypt_data(key, data)
    
    encapsulated_data = [enc_session_key, nonce, tag, ciphertext]
    
    data = pickle.dumps(encapsulated_data)
    
    stream = bytes(data)
    stream_length = len(stream)
    socket.sendall(struct.pack("<Q", stream_length))
    socket.sendall(stream)


def encrypt_data(key, data):
    recipient_key = key
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)

    return enc_session_key, cipher_aes.nonce, tag, ciphertext
    
def decrypt_data(enc_session_key, nonce, tag, ciphertext):
    if not os.path.exists(PRIVATE_PATH):
        return None

    private_key = RSA.import_key(open(PRIVATE_PATH).read())

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)

    return data
