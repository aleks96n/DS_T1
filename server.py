import socket
import os
from _thread import *
from DHT import Node
from DHT import DHT
#https://codezup.com/socket-server-with-multiple-clients-model-multithreading-python/?fbclid=IwAR33QdIbqylXP0wAq8YdESL59zZ_0c9BHuzbSw2JRbVlTJwwzLpgMhkBrkg

Server = socket.socket()
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
ThreadCount = 0
Server.bind((HOST,PORT))
print("Waiting...")
#does what?
Server.listen(5)

def readFile(fileName):
    upper, lower = None, None
    node_list = []
    shortCut_ = None
    nodeCheck, keyCheck, shortcutCheck = False, False, False

    #very naive, but works
    with open(fileName, 'r') as f:
        for line in f:
            if(line.startswith("#k")):
                keyCheck = True
                continue
            elif(line.startswith("#n")):
                nodeCheck = True
                continue
            elif(line.startswith("#s")):
                shortcutCheck = True
                continue
            if(nodeCheck):
                helper = line.split(",")
                node_list.extend(int(i) for i in helper)
                nodeCheck = False
            elif(keyCheck):
                helper = line.split(",")
                upper, lower = int(helper[1]), int(helper[0])
                keyCheck = False
            elif(shortcutCheck):
                shortCut_ = line.split(",")
                shortcutCheck = False

    return DHT(node_list,shortCut_, upper, lower)

def threaded_client(connection):
    connection.send(str.encode('Welcome to the Servern'))
    dht = None
    while True:
        data = connection.recv(2048)
        data = data.decode('utf-8')
        reply = None
        try:
            if(data.startswith("import")):
                dht = readFile(data.split(" ")[1])
                dht.list()
                reply = 'Server Says: File read'
            elif(data.startswith("join")):
                dht.join(int(data.split(" ")[1]))
                reply = 'Server Says: Joined node'
            elif(data.startswith("list")):
                dht.list()
                print(" ")
            elif(data.startswith("leave")):
                dht.leave(int(data.split(" ")[1]))
                reply = 'Server Says: Node left'
            elif(data.startswith("shortcut")):
                helper = data.split(" ")
                from_ = int(helper[1])
                to = int(helper[2])
                dht.shortcut(from_, to)
                reply = 'Server Says: Shortcut addded, use List'
            elif(data.startswith("lookup")):
                helper = data.split(" ")
                from_ = int(helper[1])
                to = int(helper[2])
                dht.lookup(from_, to)
                reply = 'Server Says: Lookup performed'
            elif(data.startswith("exit")):
                reply = 'Exiting...'
                break
            if not data:
                break
        except:
            print("Something went horribly wrong")
        if reply == None:
            reply = 'Unknown command'
        connection.sendall(str.encode(reply))
    connection.close()

"""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
"""

while True:
    Client, address = Server.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    print("Thread Number: " + str(ThreadCount))
Server.close(0)