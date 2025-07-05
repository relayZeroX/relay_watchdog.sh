import tkinter as tk
from tkinter import filedialog, messagebox
import random
import socket
import threading
import os
import string

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
        # Simulate TCP connection
        device.receive_data(data, self.ip, "TCP")

    def _send_udp(self, data, device):
        # Simulate UDP connection
        device.receive_data(data, self.ip, "UDP")

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

        # Send Data Button
        self.send_button = tk.Button(root, text="Send Random Text", command=self.send_text)
        self.send_button.pack()

        # Send File Button
        self.send_file_button = tk.Button(root, text="Send File", command=self.send_file)
        self.send_file_button.pack()

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
            # Connect to the last added device
            self.devices[-1].connect(new_device)

        self.devices.append(new_device)
        self.console.insert(tk.END, f"Added {device_type} with IP {ip} and MAC {mac}\n")

    def send_text(self):
        if len(self.devices) < 2:
            messagebox.showwarning("Simulation Error", "At least two devices are required.")
            return

        text = generate_random_text(20)  # Generates a random string of 20 characters
        protocol = self.protocol_var.get()

        src_device = self.devices[0]
        dest_device_ip = self.devices[1].ip

        src_device.send_data(text, dest_device_ip, protocol)

    def send_file(self):
        if len(self.devices) < 2:
            messagebox.showwarning("Simulation Error", "At least two devices are required.")
            return

        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        
        with open(file_path, "rb") as file:
            file_data = file.read()

        protocol = self.protocol_var.get()

        src_device = self.devices[0]
        dest_device_ip = self.devices[1].ip

        src_device.send_data(f"File: {os.path.basename(file_path)}", dest_device_ip, protocol)
        src_device.send_data(file_data, dest_device_ip, protocol)

# Main Loop
root = tk.Tk()
app = NetworkSimulatorApp(root)
root.mainloop()
