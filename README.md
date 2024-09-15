# Welcome to LANDrive 🖥-🖥-🖥

This is a concurrent client server program that accomplishes file sharing and editing files between multiple users on a local system. It is also able to run on a LAN network using the IPv4 address of the local machine which is running the server. 

I created this project for a college course, CSCI 3240: Introduction to Computer Systems.
        
1. Python Version:

   `3.12.3`

2. Packages used: 

   `PySide6 (pip install PySide6)`
  
3. Standard libraries that should already be installed:
  
    `datetime
    enum
    json
    os
    pathlib
    pickle
    platformdirs
    socket
    shutil
    struct
    sys
    tempfile
    threading
    time`


## File tree:

    LANDrive/
        client/
            __init__.py
            Upload.py
            UserInterface.py
            shared.py
            client.py
        server/
            FileDirectory/
                binary_test/
                    random.dll
                grocerylist.txt
                testfile.txt
            shared.py
            server.py

## How to run:

1. Clone the repository.

2. Ensure all the files are in the file tree noted above.
    
3. Install PySide6 if you have not already (pip install PySide6).
    
4. Run the server.py file in the server/ directory. 
    
5. Run multiple instances of the client.py file in the client/ directory.


## How to exit the program: 
    
1. client.py: 
   - Click the X in the top right corner of the program.
    
2. server.py:
    * Unfortunately, CTRL + C will not exit the python program.
        
    * Find the process id by doing ps -ef or by attempting to close the window.
    * Run kill [pid]. 

    * If that does not work, go into your task manager and end the python task process.


## Potential errors to note:

1. Non-updated server files usually means you have to manually click refresh.
    
2. Creating a directory must be unique. 
    
3. Spamming any buttons may cause the program to have issues. 
    
4. Uploading an extremely large file is untested.

5. Making changes in the shared.py file must be copied to the client/ and server/ directories

6. Port 8504 might be in use.

## Flaws
1. Insecure
2. Unfinished

## Acknowledgements
I would like to thank my professor, Dr. Sainju for his incredible teaching. Learning about client server programming was very challenging, but he was patient and made the content easy to understand. 

## Photos
Connect Screen:
![image](https://github.com/elijahxz/LANDrive/assets/98658210/e808a1b1-9dd3-4338-b192-e8314b2f91d8)
Main Screen:
![image](https://github.com/elijahxz/LANDrive/assets/98658210/5064f7ba-19ac-4096-b63e-cb7af87b0372)
Edit Screen:
![image](https://github.com/elijahxz/LANDrive/assets/98658210/53ff63a5-4c38-4982-a216-7aafb9c402c6)


