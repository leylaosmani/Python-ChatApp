import socket
import tkinter as tk
from threading import Thread


class ChatClient:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.gui = ChatGUI(self.send_message)

        # Start a new thread to handle incoming messages
        receive_thread = Thread(target=self.receive_message)
        receive_thread.start()

        # Start the main loop for the GUI
        self.gui.mainloop()

    def send_message(self, message):
        self.sock.send(message.encode())
        self.gui.display_message('me > ' + message)

    def receive_message(self):
        while True:
            try:
                message = self.sock.recv(1024).decode()
                self.gui.display_message('server > ' + message)
            except OSError:
                break


class ChatGUI(tk.Tk):
    def __init__(self, send_callback):
        super().__init__()

        self.send_callback = send_callback

        self.title("Chat Client")
        self.messages_frame = tk.Frame(self)
        self.scrollbar = tk.Scrollbar(self.messages_frame)
        self.message_list = tk.Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.message_list.pack()
        self.messages_frame.pack()

        self.message_entry = tk.Entry(self, width=50)
        self.message_entry.pack()
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack()

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message.strip():
            self.message_entry.delete(0, tk.END)
            self.send_callback(message)

    def display_message(self, message):
        self.message_list.insert(tk.END, message)


if __name__ == "__main__":
    host = input("Enter server IP address: ")
    port = 1234
    username = input("Enter your username: ")
    client = ChatClient(host, port, username)