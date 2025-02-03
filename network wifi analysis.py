import tkinter as tk
import psutil
import time

def get_network_stats():
    stats = {}
    for iface, data in psutil.net_io_counters(pernic=True).items():
        stats[iface] = {
            "Bytes Sent": data.bytes_sent,
            "Bytes Received": data.bytes_recv,
            "IP Address": psutil.net_if_addrs()[iface][0].address,
            "Last Updated": time.ctime(),
        }
    return stats

def refresh_stats():
    stats = get_network_stats()
    stats_text.delete(1.0, tk.END)
    for iface, data in stats.items():
        stats_text.insert(tk.END, f"Interface: {iface}\n")
        for key, value in data.items():
            stats_text.insert(tk.END, f"{key}: {value}\n")
        stats_text.insert(tk.END, "\n")

# Create the main window
root = tk.Tk()
root.title("Network Adapter Statistics")

# Create a text widget to display network stats
stats_text = tk.Text(root)
stats_text.pack()

# Create a button to refresh network stats
refresh_button = tk.Button(root, text="Refresh", command=refresh_stats)
refresh_button.pack()

# Display initial network stats
refresh_stats()

# Start the GUI event loop
root.mainloop()