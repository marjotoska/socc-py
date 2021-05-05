import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    # now our endpoint knows about the OTHER endpoint.
    print ("Waiting on connection...")
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    while True:
        data = clientsocket.recv(1024).decode()
        if not data:
            break
        clientsocket.send(data.encode())
        
    #clientsocket.send(bytes("Hey there, talking from server!!!","utf-8"))
    clientsocket.close()
