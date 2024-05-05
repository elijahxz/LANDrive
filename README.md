Welcome to my LANDrive project, I hope you enjoy it!

This program uses Python and PySide6 to create a server with files that runs over localhost. 

YouTube Video Link:
    https://youtu.be/-B3MIx8TpZY

Python Version:
    3.12.3

Packages used: (pip install <package>) 
  PySide6
  
  Standard libraries that should already be installed:
    datetime
    enum
    json
    os
    pathlib
    pickle
    socket
    shutil
    struct
    sys
    tempfile
    threading
    time


Zipped file tree:
FinalProjectElijahAtkins/
    client/
        __init__.py
        Upload.py
        UserInterface.py
        shared.py
        client.py
    server/
        FileDirectory/
            binary_test/
            grocerylist.txt
            testfile.txt
        shared.py
        server.py

How to run:
    1. Download the zip file to your local computer.
    2. Unzip the file in the desired directory.
    3. Ensure all the files are in the file tree noted above.
    4. Install PySide6 if you have not already (pip install PySide6).
    5. Run the server.py file in the server/ directory. 
    6. Run multiple instances of the client.py file in the client/ directory.


How to exit the program: 
    client.py: 
        Click the X in the top right corner of the program.

    server.py:
        Unfortunately, CTRL + C will not exit the python program.
        
        Find the process id by doing ps -ef or by attempting to close the window.
        Run kill <pid>. 

        If that does not work, go into your task manager and end the python task process.


Potential errors to note:
    1. Non-updated server files usually means you have to manually click refresh
    2. Creating a directory must be unique. 
    3. Spamming any buttons may cause the program and server to have issues. 
    4. Uploading an extremely large file is untested.
