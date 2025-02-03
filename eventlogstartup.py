import tkinter as tk
from tkinter import scrolledtext
import win32evtlog

def extract_startup_event_logs(event_id):
    hand = win32evtlog.OpenEventLog(None, "System")
    events = []
    while True:
        events_batch = win32evtlog.ReadEventLog(hand, win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ, 0)
        if not events_batch:
            break
        for event in events_batch:
            if event.EventID == event_id:
                events.append(event)
    win32evtlog.CloseEventLog(hand)
    return events

def display_startup_events():
    event_id = 0  # Event ID corresponding to startup apps
    startup_events = extract_startup_event_logs(event_id)
    
    result_text.delete(1.0, tk.END)  # Clear previous results
    
    result_text.insert(tk.END, f"Total matching startup events found: {len(startup_events)}\n\n")
    for event in startup_events:
        result_text.insert(tk.END, f"Event ID: {event.EventID}\n")
        result_text.insert(tk.END, f"Event Time: {event.TimeGenerated.Format()}\n")
        result_text.insert(tk.END, f"Event Description: {event.StringInserts}\n")
        result_text.insert(tk.END, "-" * 50 + "\n")
    
    # Schedule the function to run again after one hour
    root.after(3600000, display_startup_events)  # 3600000 milliseconds = 1 hour

# Create the main UI window
root = tk.Tk()
root.title("Startup Event Log Analyzer")

# Create a text area to display the analysis results
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
result_text.pack()

# Start the GUI event loop
root.after(0, display_startup_events)  # Call the function immediately on startup
root.mainloop()
