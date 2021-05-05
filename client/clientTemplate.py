# 
# Import socket library and Hash(MD5) library
#
from socket import *
import hashlib
import os
#
# Generate md5 hash function
#
def generate_md5_hash (file_data):
    md5_hash = hashlib.md5(file_data)
    f_id = md5_hash.hexdigest()
    return str(f_id)
# 
# Define Server URL and PORT
#
serverPort = 7700
serverURL = "localhost"
# 
# Create TCP socket for future connections
#
clientSocket = socket(AF_INET, SOCK_STREAM)
# 
# Connect the client to the specified server
#
clientSocket.connect((serverURL, serverPort))
print("Client connected to server: " + serverURL + ":" + str(serverPort))
# This client implements the following scenario:
# 1. LIST_FILES

clientSocket.sendall(b'LIST_FILES')

print(clientSocket.recv(1024)) #no files

clientSocket.sendall(b'UPLOAD')

print(clientSocket.recv(1024)) #filename, filesize

clientSocket.sendall(b'The_file.jpg;' + str(os.stat('The_file.jpg').st_size).encode('utf-8'))

print(clientSocket.recv(1024)) # ready for file

#send file
f = open("The_file.jpg", "rb")
d = f.read(1024)
while(d):
    clientSocket.send(d)
    d = f.read(1024)
f.close()

#compare hashes
f = open("The_file.jpg", "rb")
id = clientSocket.recv(1024)
print(id)
my_id = generate_md5_hash(f.read()).encode('utf-8')
print(my_id)
if id == my_id:
    print("Success")
else:
    print("Fail")

clientSocket.sendall(b'LIST_FILES')

d = clientSocket.recv(1024) #file list

print(d)

id, name, size = d.decode('utf-8').split(";")

clientSocket.sendall(b'DOWNLOAD')

print(clientSocket.recv(1024)) #send file id

clientSocket.sendall(id.encode('utf-8'))

#receive file
file = open("New_file.jpg", "wb")
d = clientSocket.recv(1024)
size = int(size)
while size:
    file.write(d)
    size -= len(d)
    d = clientSocket.recv(min(1024, size))
file.close()

#compare hashes
file = open("New_file.jpg", "rb")
if id == generate_md5_hash(file.read()):
    print("Success")
else:
    print("Fail")
file.close()

#close client socket
clientSocket.close()

# 2a. UPLOAD the specified file
# 2b. Check MD5
# 3. LIST_FILES
# 4a. DOWNLOAD the previously uploaded file
# 4b. Check MD5
#
#close TCP connection
