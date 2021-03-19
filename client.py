import socket
from DHT import Node
from DHT import DHT
from _thread import *


Client = socket.socket()
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
"""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)
    while True:
        command = input("Command>> ")
        command = command.lower()
        print(command)
        s.sendall(command.encode(encoding="UTF-8"))
        DHT.main()
"""
print("Waiting for connection")
Client.connect((HOST, PORT))

Response = Client.recv(1024)
while True:
	Input = input('Say something: ')
	#assume clinet gives file name
	Client.send(str.encode(Input))
	Response = Client.recv(1024)
	print(Response.decode('utf-8'))

Client.close()

