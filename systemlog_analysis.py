import tkinter as tk
from tkinter import ttk
import win32evtlog
from datetime import datetime, timedelta

class EventLogViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Log Viewer")

        self.create_ui()

    def create_ui(self):
        self.log_combo = ttk.Combobox(self.root, values=["Application", "Security", "System"])
        self.log_combo.set("Application")
        self.log_combo.pack(pady=10)

        self.load_button = ttk.Button(self.root, text="Load Logs", command=self.load_logs)
        self.load_button.pack(pady=5)

        self.log_text = tk.Text(self.root, wrap=tk.WORD, height=20, width=80)
        self.log_text.pack(padx=10, pady=10)

    def load_logs(self):
        log_type = self.log_combo.get()
        logs = self.get_event_logs(log_type)
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, logs)

    def get_event_logs(self, log_type):
        hand = win32evtlog.OpenEventLog(None, log_type)
        events = win32evtlog.ReadEventLog(hand, win32evtlog.EVENTLOG_BACKWARDS_READ |
                                          win32evtlog.EVENTLOG_SEQUENTIAL_READ, 0)

        log_entries = []
        for event in events:
            if self.is_event_recent(event):
                log_entries.append(self.format_event(event))

        return "\n\n".join(log_entries)

    def is_event_recent(self, event):
        one_month_ago = datetime.now() - timedelta(days=30)
        return event.TimeGenerated > one_month_ago

    def format_event(self, event):
        return f"Event ID: {event.EventID}\nTime Generated: {event.TimeGenerated}\n"\
               f"Computer Name: {event.ComputerName}\nMessage: {event.StringInserts}\n" + "-" * 80

def main():
    root = tk.Tk()
    app = EventLogViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
