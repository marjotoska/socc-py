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
serverSocket = socket(AF_INET, SOCK_STREAM)
# 
# Bind URL and Port to the created socket
#
serverSocket.bind((serverURL, serverPort))
# 
# Start listening for incoming connection (1 client at a time)
#
serverSocket.listen(1)
print("Server is listening on port: " + str(serverPort))


while True:
    # 
    # Accept incoming client connection
    #
    connectSocket, addr = serverSocket.accept()
    print("Client connected: " + str(addr))
    
    while True:
        data = connectSocket.recv(4096)
        print(data)

        if data == b'LIST_FILES':
            files = [f for f in os.listdir('.') if (os.path.isfile(f) and f != 'serverTemplate.py')]

            if not files:
                connectSocket.sendall(b'NO FILES AVAILABLE')
            else:
                msg = ''
                for filename in files:
                    content = open(filename, 'rb').read()
                    id = generate_md5_hash(content)
                    size = len(content)
                    msg += str(id) + ';' + filename + ';' + str(size) + '\n'
                connectSocket.sendall(msg.encode('utf-8'))

        if data == b'UPLOAD':
            connectSocket.sendall(b'FILENAME AND FILESIZE?')
            name, size = connectSocket.recv(1024).decode('utf-8').split(';')
            print(name, size)
            connectSocket.sendall(b'READY FOR FILE')

            # receive file
            file = open(name, "wb")
            d = connectSocket.recv(1024)
            while (d):
                print(d)
                file.write(d)
                d = connectSocket.recv(1024)
            file.close()

            file = open(name, "rb")
            print("calc hash")
            hash = generate_md5_hash(file.read())
            print("calculated hash")
            file.close()

            connectSocket.sendall(hash.encode('utf-8'))

        if data == b'DOWNLOAD':
            connectSocket.send(b'FILE ID?')
            id = connectSocket.recv(1024).decode('utf-8')
            print(id)

            #find file
            for f in os.listdir('.'):
                file = open(f, "rb")
                if os.path.isfile(f) and id == generate_md5_hash(file.read()):
                    target = f
                file.close()

            #send file
            file = open(f, "rb")
            d = f.read(1024)
            while (d):
                connectSocket.send(d)
                d = f.read(1024)
            file.close()

    
#close TCP connection
connectSocket.close()
