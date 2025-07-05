import socket
from scapy.all import sniff
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

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Client PC - Protocol Sender")

        self.dispatcher = EventDispatcher()
        self.dispatcher.register_handler("packet_captured", self.handle_packet_captured)
        self.dispatcher.register_handler("error_occurred", self.handle_error_occurred)

        tk.Label(root, text="Monitor IP:").pack()
        self.ip_entry = tk.Entry(root)
        self.ip_entry.pack()

        tk.Label(root, text="Monitor Port:").pack()
        self.port_entry = tk.Entry(root)
        self.port_entry.pack()

        self.start_button = tk.Button(root, text="Start Capturing", command=self.start_sniffing)
        self.start_button.pack()

        self.console = tk.Text(root, height=20, width=80)
        self.console.pack()

    def log_event(self, event):
        self.console.insert(tk.END, event + "\n")
        self.console.yview(tk.END)

    def start_sniffing(self):
        monitor_ip = self.ip_entry.get()
        monitor_port = int(self.port_entry.get())
        thread = Thread(target=self.sniff_and_send, args=(monitor_ip, monitor_port))
        thread.daemon = True
        thread.start()

    def sniff_and_send(self, monitor_ip, monitor_port):
        try:
            def process_packet(packet):
                packet_info = self.parse_packet(packet)
                if packet_info:
                    self.dispatcher.dispatch_event("packet_captured", packet_info)
                    self.send_data_to_monitor(monitor_ip, monitor_port, packet_info)

            sniff(prn=process_packet, store=0)  # Capture packets and process them with process_packet

        except Exception as e:
            self.dispatcher.dispatch_event("error_occurred", str(e))

    def send_data_to_monitor(self, monitor_ip, monitor_port, packet_info):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_sock:
                send_sock.connect((monitor_ip, monitor_port))
                send_sock.sendall(packet_info.encode('utf-8'))
        except Exception as e:
            self.dispatcher.dispatch_event("error_occurred", str(e))

    def parse_packet(self, packet):
        if packet.haslayer('IP'):
            ip_src = packet['IP'].src
            ip_dst = packet['IP'].dst
            protocol = packet['IP'].proto

            if protocol == 6:  # TCP
                return f"TCP Packet: Source IP: {ip_src}, Dest IP: {ip_dst}"
            elif protocol == 17:  # UDP
                return f"UDP Packet: Source IP: {ip_src}, Dest IP: {ip_dst}"

        return "Non-IP Packet"

    def handle_packet_captured(self, packet_info):
        self.log_event(f"Captured: {packet_info}")

    def handle_error_occurred(self, error_message):
        self.log_event(f"Error: {error_message}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
