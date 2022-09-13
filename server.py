import socket
import os
import threading
import hashlib
import json

from dataclasses import dataclass
from pymarshaler.marshal import Marshal

@dataclass
class User:
    username: str
class Password:
    password: str


# Create Socket (TCP) Connection
ServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM) 
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:    
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)
HashTable = {}

# Function : For each client 
def threaded_client(connection):
    connection.send(str.encode(' Username & Password : ')) # Request Username dan Password dari client
    name, password = connection.recv(2048).split() # Menerima Username dan Password dari client yang dijadikan satu pengiriman dan di split
    password = password.decode() # Proses decode password
    name = name.decode() # Proses decode username
    marshalUname = Marshal.marshal(name)
    marshalPass = Marshal.marshal(password)
    print(marshalUname, marshalPass)

# Fase pendaftaran   
# If user,  maka akan masuk ke Hashtable Dictionary  
    if name not in HashTable:
        HashTable[name]=password
        connection.send(str.encode('Registeration Successful!')) 
        print('Registered :',name)
        print("{:<20} {:<8}".format('USER','PASSWORD'))
        
        for k, v in HashTable.items():
            label, num = k,v
            print("{:<20} {:<8}".format(label, num))
        print("-------------------------------------------")
        
    else:
# If already existing user, check if the entered password is correct
        if(HashTable[name] == password):
            connection.send(str.encode('Clear')) # Response Code yang tampil pada client 
            print('Connected : ',name, password)
        else:
            connection.send(str.encode('Login Failed')) # Response code for ketika gagal login
            print('Connection denied : ',name, password)
    while True:
        break
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    client_handler = threading.Thread(
        target=threaded_client,
        args=(Client,)  
    )
    client_handler.start()
    ThreadCount += 1
    print('Connection Request: ' + str(ThreadCount))
ServerSocket.close()



#decode dan endoce paket lebih kecil
#format digunakan untuk mengecek mana user dan pasword, atau mengecek string
#HashTable menggunakan arry sebagai penyimpanan, dan berfungsi sebagai
#struktur data dimana operasi penyisipan dan pencarianndata sangat cepat