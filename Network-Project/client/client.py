import time, socket, sys
from gui_client import ChatClient

print('Client Server...')
time.sleep(1)

# Get the hostname, IP Address from socket and set Port
soc = socket.socket()
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
print(shost, '({})'.format(ip))

# Get information to connect with the server
server_host = input('Enter server\'s IP address:')
name = input('Enter Client\'s name: ')
port = 1234
print('Trying to connect to the server: {}, ({})'.format(server_host, port))
time.sleep(1)
soc.connect((server_host, port))
print("Connected...\n")

# Send the name of the client to the server
soc.send(name.encode())

# Receive the server name
server_name = soc.recv(1024)
server_name = server_name.decode()

print('{} has joined...'.format(server_name))
print('Enter bye to exit.')

# Start the chat client with the given server information
client = ChatClient(server_host, port, name, server_name, soc)

# Start the main loop for sending and receiving messages
while True:
    message = soc.recv(1024)
    message = message.decode()
    print(server_name, ":", message)
    message = input(str("Me : "))
    if message == "bye":
        message = "Leaving the chat room..."
        soc.send(message.encode())
        print("\n")
        break
    soc.send(message.encode())