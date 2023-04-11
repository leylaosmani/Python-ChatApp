import socket
import tkinter as tk
from gui_server import ServerGUI

print('Setup Server...')

server_gui = ServerGUI()

name = server_gui.name
connection = server_gui.connection
client_name = server_gui.client_name

while True:
    message = input()
    if message == 'bye':
        message = 'Goodbye...'
    
    connection.send(message.encode())

    if message == 'Goodbye...':
        print("\n")
        break

    message = connection.recv(1024)
    message = message.decode()
    server_gui.message_listbox.insert(tk.END, f"{client_name} > {message}\n")

connection.close()