 NETWORK PROTOCOL SIMULATOR

This is a GUI-based **Network Protocol Simulator** built in Python using `tkinter`. The simulator allows you to add virtual network devices, assign them IP/MAC addresses, connect them randomly, send data using TCP or UDP, and visualize network activity and topology.

💡 Features

- Create devices with random or custom IP and MAC addresses
- Automatically connect new devices to existing ones
- Send data using TCP or UDP protocol
- Display logs in a console (inside the GUI)
- Visualize:
  - 📊 Bar Graph showing number of connections per device
  - 📈 Sinusoidal Graph showing devices plotted over a sine curve

🛠️ Technologies Used

- Python 3.x
- `tkinter` – for GUI
- `matplotlib` – for graph plotting
- `numpy` – for sine wave generation
- `networkx` – included for possible future extension (currently unused in plotting)
- Standard libraries: `random`, `string`

📂 Project Structure

network_simulator/
├── main.py # Main application file
├── README.md # This file

shell
Copy
Edit

🚀 Getting Started

 ✅ Prerequisites

Make sure you have Python installed (3.x). Then install the required libraries:

```bash
pip install matplotlib numpy networkx
🧪 Running the App
bash
Copy
Edit
python main.py
🖱 GUI Functions:
Click Randomize to auto-fill IP/MAC

Click Connect to add a device (it auto-connects to a random existing device)

Select TCP or UDP for sending data

Click Show Network Graph:

"Yes" = Bar Graph

"No" = Sinusoidal Graph

📊 Sample Output
(You can add screenshots here after running the app)

🌟 Future Improvements
Manual connection between selected devices

Real-time packet animation

Save/load network setups

Use networkx for network topology visualization

Error simulation (e.g., packet loss in UDP)

👩‍💻 Author
Dharshini
(https://github.com/dharshini1504)

