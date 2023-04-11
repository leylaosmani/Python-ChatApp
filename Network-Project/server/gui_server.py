import tkinter as tk
import threading
import socket


class ServerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Server")
        self.window.resizable(False, False)

        self.message_listbox = tk.Listbox(self.window, height=15, width=50)
        self.message_listbox.pack(side=tk.TOP, padx=5, pady=5)

        self.message_entry = tk.Entry(self.window, width=50)
        self.message_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.send_button = tk.Button(self.window, text="Send", command=self.send_message)
        self.send_button.pack()

        self.host_name = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.host_name)
        self.port = 1234
        self.name = "Server"

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host_name, self.port))

        self.message_listbox.insert(tk.END, f"Setup Server...\n{self.host_name} ({self.ip_address})\n")
        self.message_listbox.insert(tk.END, "Waiting for incoming connections...\n")

        self.connection = None
        self.client_name = None

        self.accept_thread = threading.Thread(target=self.accept_connections)
        self.accept_thread.start()

        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.window.mainloop()

    def accept_connections(self):
        self.server_socket.listen(1)
        self.connection, addr = self.server_socket.accept()
        self.message_listbox.insert(tk.END, f"Received connection from {addr[0]} ({addr[1]})\n")
        self.message_listbox.insert(tk.END, f"Connection Established. Connected From: {addr[0]}, ({addr[1]})\n")
        self.client_name = self.connection.recv(1024).decode()
        self.message_listbox.insert(tk.END, f"{self.client_name} has connected.\n")
        self.connection.send(self.name.encode())

        while True:
            message = self.connection.recv(1024).decode()
            if message == "bye":
                break
            self.message_listbox.insert(tk.END, f"{self.client_name} > {message}\n")

    def send_message(self):
        message = self.message_entry.get()
        if message == "bye":
            self.connection.send(message.encode())
            self.close_window()
        else:
            self.message_listbox.insert(tk.END, f"{self.name} > {message}\n")
            self.connection.send(message.encode())
            self.message_entry.delete(0, tk.END)
            self.send_button.config(text="Sent!")
            self.window.after(1000, lambda: self.send_button.config(text="Send"))

    def close_window(self):
        self.server_socket.close()
        self.window.destroy()


if __name__ == "__main__":
    ServerGUI()