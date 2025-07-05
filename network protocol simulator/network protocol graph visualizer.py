import tkinter as tk
from tkinter import filedialog, messagebox
import random
import string
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np  # Added for sine plot

# Function to generate random text
def generate_random_text(length=20):
    letters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(letters) for _ in range(length))

# Helper Functions
def random_ip():
    return f"192.168.0.{random.randint(2, 254)}"

def random_mac():
    return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))

# Main Device Class
class Device:
    def __init__(self, ip, mac, device_type, console):
        self.ip = ip
        self.mac = mac
        self.device_type = device_type
        self.connections = []
        self.console = console
    
    def log_event(self, event):
        self.console.insert(tk.END, f"{self.device_type} ({self.ip}): {event}\n")
        self.console.yview(tk.END)
    
    def connect(self, other_device):
        self.connections.append(other_device)
        other_device.connections.append(self)
        self.log_event(f"Connected to {other_device.device_type} ({other_device.ip})")
    
    def send_data(self, data, destination_ip, protocol):
        self.log_event(f"Sending data to {destination_ip} using {protocol} protocol")
        for device in self.connections:
            if device.ip == destination_ip:
                if protocol == "TCP":
                    self._send_tcp(data, device)
                elif protocol == "UDP":
                    self._send_udp(data, device)
                return
        self.log_event(f"Destination {destination_ip} not found.")
    
    def receive_data(self, data, source_ip, protocol):
        self.log_event(f"Received data from {source_ip} using {protocol} protocol: {data}")

    def _send_tcp(self, data, device):
        device.receive_data(data, self.ip, "TCP")

    def _send_udp(self, data, device):
        device.receive_data(data, self.ip, "UDP")

# Main GUI Class
class NetworkSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Protocol Simulator")

        # Console Output
        self.console = tk.Text(root, height=10, width=60)
        self.console.pack()

        # Device Configuration
        tk.Label(root, text="IP:").pack()
        self.ip_entry = tk.Entry(root)
        self.ip_entry.pack()

        tk.Label(root, text="MAC:").pack()
        self.mac_entry = tk.Entry(root)
        self.mac_entry.pack()

        tk.Label(root, text="Device Type:").pack()
        self.device_type_entry = tk.Entry(root)
        self.device_type_entry.pack()

        # Randomize Button
        self.randomize_button = tk.Button(root, text="Randomize", command=self.randomize_addresses)
        self.randomize_button.pack()

        # Connect Button
        self.connect_button = tk.Button(root, text="Connect", command=self.connect_device)
        self.connect_button.pack()

        # Protocol Selection
        self.protocol_var = tk.StringVar(value="TCP")
        tk.Label(root, text="Select Protocol:").pack()
        tk.Radiobutton(root, text="TCP", variable=self.protocol_var, value="TCP").pack()
        tk.Radiobutton(root, text="UDP", variable=self.protocol_var, value="UDP").pack()

        # Show Network Graph Button
        self.show_graph_button = tk.Button(root, text="Show Network Graph", command=self.show_graph)
        self.show_graph_button.pack()

        # Placeholder for devices
        self.devices = []

    def randomize_addresses(self):
        self.ip_entry.delete(0, tk.END)
        self.ip_entry.insert(0, random_ip())

        self.mac_entry.delete(0, tk.END)
        self.mac_entry.insert(0, random_mac())

    def connect_device(self):
        ip = self.ip_entry.get()
        mac = self.mac_entry.get()
        device_type = self.device_type_entry.get()

        if not ip or not mac or not device_type:
            messagebox.showwarning("Input Error", "All fields must be filled!")
            return

        new_device = Device(ip, mac, device_type, self.console)
        if self.devices:
            random_device = random.choice(self.devices)
            random_device.connect(new_device)

        self.devices.append(new_device)
        self.console.insert(tk.END, f"Added {device_type} with IP {ip} and MAC {mac}\n")

    def show_graph(self):
        choice = messagebox.askquestion("Graph Type", "Show Bar Graph instead of Network Graph? (Yes = Bar Graph, No = Sinusoidal Graph)")

        device_ips = [device.ip for device in self.devices]
        connection_counts = [len(device.connections) for device in self.devices]

        plt.figure(figsize=(10, 6))

        if choice == 'yes':
            # Bar Graph: Number of connections per device
            plt.bar(device_ips, connection_counts, color='skyblue')
            plt.xlabel('Device IP')
            plt.ylabel('Number of Connections')
            plt.title('Connections per Device')
        else:
            # Sinusoidal Graph: Device IPs mapped along a sine wave
            x = np.arange(len(self.devices))
            y = np.sin(x)
            plt.plot(x, y, 'bo-', label='Device Position')
            for i, ip in enumerate(device_ips):
                plt.text(x[i], y[i] + 0.1, ip, ha='center')
            plt.title('Devices on Sinusoidal Path')
            plt.xlabel('Device Index')
            plt.ylabel('Sin(y)')

        plt.grid(True)
        plt.tight_layout()
        plt.show()

# Main Loop
root = tk.Tk()
app = NetworkSimulatorApp(root)

# Create more than 5 devices and connect them
for _ in range(6):
    app.connect_device()

root.mainloop()
