import tkinter as tk
from tkinter import scrolledtext
import win32evtlog
import win32evtlogutil

class EventLogViewerApp:
    def __init__(self, root):
        
        self.root = root
        self.root.title("Event Log Viewer")

        self.event_id_entry = tk.Entry(root)
        self.event_id_entry.pack()

        self.display_all_button = tk.Button(root, text="Display All Events", command=self.display_all_events)
        self.display_all_button.pack()

        self.display_button = tk.Button(root, text="Display Searched Event", command=self.display_searched_event)
        self.display_button.pack()

        self.result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.result_text.pack()

    def get_all_events(self):
        hand = win32evtlog.OpenEventLog(None, "System")
        events = []

        while True:
            events_batch = win32evtlog.ReadEventLog(hand, win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ, 0)
            if not events_batch:
                break
            events.extend(events_batch)
        win32evtlog.CloseEventLog(hand)
        return events

    def get_filtered_event(self, event_id):
        hand = win32evtlog.OpenEventLog(None, "System")
        events = []

        while True:
            events_batch = win32evtlog.ReadEventLog(hand, win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ, 0)
            if not events_batch:
                break
            for event in events_batch:
                if event.EventID == event_id:
                    events.append(event)
                elif event.EventID < event_id:
                    # Events are in chronological order, so if the event ID is smaller than specified, we can break
                    break
        win32evtlog.CloseEventLog(hand)
        return events

    def display_all_events(self):
        all_events = self.get_all_events()

        self.result_text.delete(1.0, tk.END)  # Clear previous results

        if all_events:
            self.result_text.insert(tk.END, f"Total events found: {len(all_events)}\n\n")
            for event in all_events:
                self.result_text.insert(tk.END, f"Event ID: {event.EventID}\n")
                self.result_text.insert(tk.END, f"Event Time: {event.TimeGenerated.Format()}\n")
                self.result_text.insert(tk.END, f"Event Source: {event.SourceName}\n")
                self.result_text.insert(tk.END, f"Event Description: {win32evtlogutil.SafeFormatMessage(event)}\n")
                self.result_text.insert(tk.END, "-" * 50 + "\n")
        else:
            self.result_text.insert(tk.END, "No events found.\n")

    def display_searched_event(self):
        try:
            event_id = int(self.event_id_entry.get())

            filtered_event = self.get_filtered_event(event_id)

            self.result_text.delete(1.0, tk.END)  # Clear previous results

            if filtered_event:
                self.result_text.insert(tk.END, f"Total matching events found: {len(filtered_event)}\n\n")
                for event in filtered_event:
                    self.result_text.insert(tk.END, f"Event ID: {event.EventID}\n")
                    self.result_text.insert(tk.END, f"Event Time: {event.TimeGenerated.Format()}\n")
                    self.result_text.insert(tk.END, f"Event Source: {event.SourceName}\n")
                    self.result_text.insert(tk.END, f"Event Description: {win32evtlogutil.SafeFormatMessage(event)}\n")
                    self.result_text.insert(tk.END, "-" * 50 + "\n")
            else:
                self.result_text.insert(tk.END, "No matching events found.\n")

        except ValueError:
            self.result_text.insert(tk.END, "Invalid Event ID format. Please enter a valid Event ID.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = EventLogViewerApp(root)
    root.mainloop()
