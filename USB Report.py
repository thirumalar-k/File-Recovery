import tkinter as tk
import os
import time
import win32evtlog

def generate_usb_report():
    current_time = time.strftime("%Y-%m-%d %H-%M-%S")
    report_file = f"usb_report_{current_time}.txt"
    report_text = ""

    event_log = win32evtlog.OpenEventLog(None, "System")
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    events = win32evtlog.ReadEventLog(event_log, flags, 0)

    thirty_days_ago = (time.time() - 30 * 24 * 60 * 60)  # Unix timestamp

    for event in events:
        timestamp = event.TimeGenerated.Format()
        event_id = event.EventID
        event_source = event.SourceName
        event_timestamp = int(event.TimeGenerated.timestamp())
        if event_timestamp > thirty_days_ago:
            report_text += f"Timestamp: {timestamp}\n"
            report_text += f"Event Source: {event_source}\n"
            report_text += f"Event ID: {event_id}\n\n"

    win32evtlog.CloseEventLog(event_log)

    if report_text:
        with open(report_file, "w") as f:
            f.write("USB Device Attachment Report (Last 30 Days)\n")
            f.write(report_text)
        report_status.set(f"Report generated: {report_file}")
    else:
        report_status.set("No USB device attachment events found in the last 30 days.")

# Create the main window
root = tk.Tk()
root.title("USB Device Attachment Report")

# Create a button to generate the report
generate_button = tk.Button(root, text="Generate USB Report (Last 30 Days)", command=generate_usb_report)
generate_button.pack()

# Create a label to display report status
report_status = tk.StringVar()
report_label = tk.Label(root, textvariable=report_status)
report_label.pack()

# Start the GUI event loop
root.mainloop()
