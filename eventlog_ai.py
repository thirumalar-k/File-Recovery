import tkinter as tk
from tkinter import scrolledtext
import win32evtlog
import datetime

class EventViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Viewer")

        self.log_types = ["Application", "Security", "System"]
        
        self.log_type_combobox = tk.StringVar()
        self.log_type_combobox.set(self.log_types[0])
        self.log_type_combobox_menu = tk.OptionMenu(root, self.log_type_combobox, *self.log_types)
        self.log_type_combobox_menu.pack(pady=10)
        
        self.process_listbox = tk.Listbox(root)
        self.process_listbox.pack()

        self.log_text = scrolledtext.ScrolledText(root, height=15)
        self.log_text.pack(fill="both", expand=True)

        self.update_button = tk.Button(root, text="Update", command=self.update)
        self.update_button.pack(pady=10)

        self.update()

    def retrieve_running_processes(self):
        return ["process1", "process2", "process3"]  # Replace with actual process retrieval

    def retrieve_similar_logs(self, process_name, log_type):
        logs = []
        hand = win32evtlog.OpenEventLog(None, log_type)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        events = win32evtlog.ReadEventLog(hand, flags, 0)

        for event in events:
            event_inserts = event.StringInserts
            if event_inserts:
                event_inserts = event_inserts[0]  # Convert to string
                if process_name.lower() in event_inserts.lower():
                    event_record = {
                        "TimeGenerated": event.TimeGenerated.Format(),
                        "SourceName": event.SourceName,
                        "EventID": event.EventID,
                        "Description": event_inserts,
                    }
                    logs.append(event_record)

        win32evtlog.CloseEventLog(hand)
        return logs

    def retrieve_normal_logs(self, log_type):
        logs = []
        hand = win32evtlog.OpenEventLog(None, log_type)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        events = win32evtlog.ReadEventLog(hand, flags, 0)

        current_time = datetime.datetime.now()
        thirty_days_ago = current_time - datetime.timedelta(days=30)

        for event in events:
            event_time = datetime.datetime.fromtimestamp(event.TimeGenerated.timestamp())
            if event_time >= thirty_days_ago:
                event_record = {
                    "TimeGenerated": event_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "SourceName": event.SourceName,
                    "EventID": event.EventID,
                    "Description": event.StringInserts,
                }
                logs.append(event_record)

        win32evtlog.CloseEventLog(hand)
        return logs

    def update(self):
        self.process_listbox.delete(0, tk.END)
        running_processes = self.retrieve_running_processes()
        for process_name in running_processes:
            self.process_listbox.insert(tk.END, process_name)

        selected_process = self.process_listbox.get(tk.ACTIVE)
        selected_log_type = self.log_type_combobox.get()
        self.log_text.delete(1.0, tk.END)

        if selected_process:
            similar_logs = self.retrieve_similar_logs(selected_process, selected_log_type)
            self.log_text.insert(tk.END, "Similar Logs:\n")
            for log in similar_logs:
                log_text = f"{log['TimeGenerated']} - {log['SourceName']} - {log['EventID']} - {log['Description']}\n"
                self.log_text.insert(tk.END, log_text)

        normal_logs = self.retrieve_normal_logs(selected_log_type)
        self.log_text.insert(tk.END, "\nNormal Logs:\n")
        for log in normal_logs:
            log_text = f"{log['TimeGenerated']} - {log['SourceName']} - {log['EventID']} - {log['Description']}\n"
            self.log_text.insert(tk.END, log_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = EventViewerApp(root)
    root.mainloop()
