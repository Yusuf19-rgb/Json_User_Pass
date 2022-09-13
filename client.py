import socket
import json



# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
# client.connect((target, port))
client.connect(('127.0.0.1', 1233))
response = client.recv(2048)
# Input UserName
name = input(response.decode())	
client.send(str.encode(name))
response = client.recv(2048)
# Input Password
password = input(response.decode())	
client.send(str.encode(password))
response = client.recv(2048)
# Receive response 
response = response.decode()

print(response)
client.close()

