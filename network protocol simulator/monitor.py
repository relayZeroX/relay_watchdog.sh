
import socket
import tkinter as tk
from threading import Thread

class EventDispatcher:
    def __init__(self):
        self._event_handlers = {}

    def register_handler(self, event_type, handler):
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)

    def dispatch_event(self, event_type, *args, **kwargs):
        if event_type in self._event_handlers:
            for handler in self._event_handlers[event_type]:
                handler(*args, **kwargs)

class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor PC - Protocol Listener")

        self.dispatcher = EventDispatcher()
        self.dispatcher.register_handler("data_received", self.handle_data_received)
        self.dispatcher.register_handler("error_occurred", self.handle_error_occurred)

        tk.Label(root, text="Listen IP:").pack()
        self.ip_entry = tk.Entry(root)
        self.ip_entry.pack()

        tk.Label(root, text="Listen Port:").pack()
        self.port_entry = tk.Entry(root)
        self.port_entry.pack()

        self.start_button = tk.Button(root, text="Start Listening", command=self.start_listening)
        self.start_button.pack()

        self.console = tk.Text(root, height=20, width=80)
        self.console.pack()

    def log_event(self, event):
        self.console.insert(tk.END, event + "\n")
        self.console.yview(tk.END)

    def start_listening(self):
        listen_ip = self.ip_entry.get()
        listen_port = int(self.port_entry.get())
        if listen_ip == '':
            listen_ip = '0.0.0.0'
        thread = Thread(target=self.listen_for_data, args=(listen_ip, listen_port))
        thread.daemon = True
        thread.start()

    def listen_for_data(self, listen_ip, listen_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
                server_sock.bind((listen_ip, listen_port))
                server_sock.listen(1)
                self.log_event(f"Listening on {listen_ip}:{listen_port}...")

                conn, addr = server_sock.accept()
                with conn:
                    self.log_event(f"Connection established with {addr}")
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            break
                        self.dispatcher.dispatch_event("data_received", data.decode('utf-8'))
        except Exception as e:
            self.dispatcher.dispatch_event("error_occurred", str(e))

    def handle_data_received(self, data):
        self.log_event(f"Received: {data}")

    def handle_error_occurred(self, error_message):
        self.log_event(f"Error: {error_message}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()
