import tkinter as tk
from tkinter import ttk
import win32evtlog

class EventLogViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows Event Log Viewer")
        
        self.tree = ttk.Treeview(root, columns=("Event ID", "Source", "Time"), show="headings") 
        self.tree.heading("Event ID", text="Event ID")
        self.tree.heading("Source", text="Source")
        self.tree.heading("Time", text="Time")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.filter_label = tk.Label(root, text="Filter by Source:")
        self.filter_label.pack()
        
        self.filter_entry = tk.Entry(root)
        self.filter_entry.pack()

        self.filter_event_id_label = tk.Label(root, text="Filter by Event ID:")  # Event ID filter label
        self.filter_event_id_label.pack()

        self.filter_event_id_entry = tk.Entry(root)  # Event ID filter entry
        self.filter_event_id_entry.pack()

        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_logs)
        self.refresh_button.pack()

    def refresh_logs(self):
        self.tree.delete(*self.tree.get_children())  # Clear existing entries

        hand = win32evtlog.OpenEventLog(None, "System")
        total_records = win32evtlog.GetNumberOfEventLogRecords(hand)

        filter_source = self.filter_entry.get().strip().lower()
        filter_event_id = self.filter_event_id_entry.get().strip()  # Get the Event ID filter input

        for i in range(total_records):
            try:
                events = win32evtlog.ReadEventLog(hand, win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ, 0)
                event = events[0]
                event_id = event.EventID
                source = event.SourceName
                time = event.TimeGenerated.Format()
                
                if (not filter_source or filter_source in source.lower()) and \
                   (not filter_event_id or str(event_id) == filter_event_id):
                    self.tree.insert("", "end", values=(event_id, source, time))
            except:
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = EventLogViewerApp(root)
    root.mainloop()
