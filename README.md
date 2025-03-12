# Welcome to LANDrive 🖥-🖥-🖥

This is a concurrent client server program that accomplishes file sharing and editing files between multiple users via TCP socket connections. 

## Photos
Connect Screen:
![image](https://github.com/user-attachments/assets/968ccbfc-4837-429a-a101-cf3efcef3d35)
Main Screen:
![image](https://github.com/elijahxz/LANDrive/assets/98658210/5064f7ba-19ac-4096-b63e-cb7af87b0372)
Edit Screen:
![image](https://github.com/elijahxz/LANDrive/assets/98658210/53ff63a5-4c38-4982-a216-7aafb9c402c6)

        
1. Python Version:

   `3.12.3`

2. Packages used: 

   `PySide6 (pip install PySide6)`
   
   `pycryptodome (pip install pycryptodome)`
   
   `platformdirs (pip install platformdirs)`

4. Standard libraries that should already be installed:
  
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
```
   ─── LANDrive/
    ├── client/
    │   ├── __init__.py
    │   ├── Upload.py
    │   ├── UserInterface.py
    │   ├── shared.py
    │   └── client.py
    └── server/
        ├── FileDirectory/
        │   ├── binary_test/
        │   │   └── random.dll
        │   ├── grocerylist.txt
        │   └── testfile.txt
        ├── shared.py
        └── server.py
```
## How to run locally
<p>
1. Clone the repository. <br>
2. Import the apropriate libraries <br>
3. Run the server.py file <br>
&nbsp;&nbsp;&nbsp;&nbsp;In a terminal, run: <b>python{3} server.py</b> <br>
&nbsp;&nbsp;&nbsp;&nbsp;Must be done in the server/ directory! <br>
4. Run the client.py file <br>
&nbsp;&nbsp;&nbsp;&nbsp;In a terminal, run: <b>python{3} client.py</b> <br>
&nbsp;&nbsp;&nbsp;&nbsp;Must be done in the client/ directory! <br>
&nbsp;&nbsp;&nbsp;&nbsp;Insert 127.0.0.1 or localhost into the Host <br>
&nbsp;&nbsp;&nbsp;&nbsp;Insert 8504 into the Port <br>
&nbsp;&nbsp;&nbsp;&nbsp;Leave the password field blank <br>
<br>
Why do these commands have to be done in their respective directories? Both the client and server generate and read their public/private keys from the directory they are called in. Additionally, the server looks for FileDirectory/.

</p>

## How to run with password protection
<p>
1. Create a file called password.pem in the server/ directory <br>
2. Insert your password into the password.pem file. <br>
3. Run the program and insert the password into the field on the connect screen. <br>

Note: This isn't the safest way to store a password on a file system, but 
it is the only way I have implemented it to work. If you would like to encrypt the password,
feel free to edit the code that reads in the password from the file. 
</p>

## How to run over LAN:
<p>
1. In server/server.py change HOST to the LAN IPv4 on device<br>
&nbsp;&nbsp;&nbsp;&nbsp;Windows: ipconfig, Linux: ifconfig or ip, Mac: not sure & untested
</p>

## How to run on a Rasberry PI
<p>
This will not go in depth, but I was able to get it running on a rasberry pi by accessing my router settings and port forwarding the port I wanted to use. I created a linux service descriptor, and specified it to run the server after an internet connection was made. 
<br>
To access the server on my Windows devices, I had to open the firewall settings and allow traffic at the designated port. While on my local network, I used an online IP finder tool to find my public IP. 
<br>
<br>
This was super fun & cool to get working on a rasberry pi. If you have a rasberry pi but have never done something like this before, I say go for it! You will learn some things about linux and networking 😄
</p>


## How to exit the program: 
<p>
1. client.py: <br>
&nbsp;&nbsp;&nbsp;&nbsp;Click the X in the top right corner of the program.<br>
2. server.py:<br>
&nbsp;&nbsp;&nbsp;&nbsp;Sometimes, CTRL + C will not exit the python program.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Find the process id by doing ps -ef and kill {-9} {pid}.<br>
&nbsp;&nbsp;&nbsp;&nbsp;If that does not work (windows), go into your task manager and end the python task process.<br>
&nbsp;&nbsp;&nbsp;&nbsp;If that does not work, try closing the terminal<br>
</p>


## Potential errors to note:
<p>
1. Not multithreaded:<br>
&nbsp;&nbsp;&nbsp;&nbsp;Users manually have to refresh files.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Uploading/Downloading large files will cause the GUI to pause. <br>
3. Creating a directory must have a unique name. <br>
4. Spamming any buttons may cause the program to have issues. <br>
5. Making changes in the shared.py file must be copied to the client/ and server/ directories<br>
6. Port 8504 might be in use.
</p>

## Flaws
<p>
1. Slow<br>
&nbsp;&nbsp;&nbsp;&nbsp;Literally everything is encrypted using RSA, which makes the program extremely slow<br>
2. Not multithreaded
</p>



## Post project reflection
<p>
This project was a lot of fun! I got to use new tools and I learned a lot. It was the first application I tested on my rasberry pi. If I were to do it again, I would make it multithreaded, implement a better/faster way for file transfers (maybe scp?), and spend a little more time on the user interface.
</p>


