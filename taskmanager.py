
import sys
import psutil
import platform
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLabel


class TaskManagerUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task Manager Replica")
        self.setGeometry(100, 100, 800, 600)

        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(20, 20, 760, 560)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["PID", "Name", "CPU %", "Memory %"])

        self.refresh_button = QPushButton("Refresh", self)
        self.refresh_button.setGeometry(20, 580, 100, 20)
        self.refresh_button.clicked.connect(self.refresh_processes)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table_widget)
        self.layout.addWidget(self.refresh_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def refresh_processes(self):
        self.table_widget.setRowCount(0)
        for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            process_info = process.info
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(str(process_info['pid'])))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(process_info['name']))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(f"{process_info['cpu_percent']:.2f}"))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(f"{process_info['memory_percent']:.2f}"))

class PerformanceReplica(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Performance Replica")
        self.setGeometry(100, 100, 600, 500)

        self.layout = QVBoxLayout()

        self.cpu_frame = self.create_info_frame()
        self.cpu_label = self.add_info_label(self.cpu_frame, "CPU Usage: ")
        self.cpu_name_label = self.add_info_label(self.cpu_frame, "CPU Name: ")
        self.layout.addWidget(self.cpu_frame)

        self.memory_frame = self.create_info_frame()
        self.memory_label = self.add_info_label(self.memory_frame, "Memory Usage: ")
        self.memory_type_label = self.add_info_label(self.memory_frame, "Memory Type: ")
        self.layout.addWidget(self.memory_frame)

        self.disk_frame = self.create_info_frame()
        self.disk_label = self.add_info_label(self.disk_frame, "Disk Usage: ")
        self.disk_type_label = self.add_info_label(self.disk_frame, "Disk Type: ")
        self.layout.addWidget(self.disk_frame)

        self.wifi_frame = self.create_info_frame()
        self.wifi_label = self.add_info_label(self.wifi_frame, "Wi-Fi SSID: ")
        self.wifi_type_label = self.add_info_label(self.wifi_frame, "Wi-Fi Type: ")
        self.layout.addWidget(self.wifi_frame)

        self.gpu_frame = self.create_info_frame()
        self.gpu_label = self.add_info_label(self.gpu_frame, "GPU Usage: ")
        self.gpu_name_label = self.add_info_label(self.gpu_frame, "GPU Name: ")
        self.layout.addWidget(self.gpu_frame)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.update_performance()

    def update_performance(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_info = self.get_cpu_info()
        memory_info = psutil.virtual_memory()
        memory_type = self.get_memory_type()
        disk_info = psutil.disk_usage('/')
        disk_type = self.get_disk_type()
        wifi_ssid, wifi_type = self.get_wifi_info()
        gpu_info, gpu_name = self.get_gpu_info()

        self.cpu_label.setText(f"CPU Usage: {cpu_percent:.2f}%")
        self.cpu_name_label.setText(f"CPU Name: {cpu_info}")
        self.memory_label.setText(f"Memory Usage: {memory_info.percent:.2f}%")
        self.memory_type_label.setText(f"Memory Type: {memory_type}")
        self.disk_label.setText(f"Disk Usage: {disk_info.percent:.2f}%")
        self.disk_type_label.setText(f"Disk Type: {disk_type}")
        self.wifi_label.setText(f"Wi-Fi SSID: {wifi_ssid}")
        self.wifi_type_label.setText(f"Wi-Fi Type: {wifi_type}")
        self.gpu_label.setText(f"GPU Usage: {gpu_info}")
        self.gpu_name_label.setText(f"GPU Name: {gpu_name}")

        #QTimer.singleShot(1000, self.update_performance)
    def add_info_label(self, frame, text):
        label = QLabel(text, frame)
        layout = frame.layout()
        layout.addWidget(label)
        return label

    def create_info_frame(self):
        frame = QWidget(self)
        frame.setStyleSheet("QFrame { border: 1px solid black; padding: 5px; }")
        layout = QVBoxLayout()
        frame.setLayout(layout)
        return frame
    
    def get_cpu_info(self):
        return platform.processor()

    def get_memory_type(self):
        return "Unknown"  # Add code to retrieve memory type if available

    def get_disk_type(self):
        return "Unknown"  # Add code to retrieve disk type if available

    def get_wifi_info(self):
        system = platform.system()
        if system == "Windows":
            return self.get_wifi_info_windows()
        elif system == "Darwin":
            return self.get_wifi_info_mac()
        elif system == "Linux":
            return self.get_wifi_info_linux()
        else:
            return "Not supported", "Not supported"

    def get_wifi_info_windows(self):
        try:
            import subprocess
            output = subprocess.check_output(["netsh", "wlan", "show", "interfaces"]).decode("utf-8")
            ssid_line = [line.strip() for line in output.splitlines() if "SSID" in line]
            ssid = ssid_line[0].split(":")[1].strip()
            return ssid, "Wi-Fi"
        except:
            return "Not connected", "Not supported"

    def get_wifi_info_mac(self):
        try:
            import subprocess
            output = subprocess.check_output(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"]).decode("utf-8")
            ssid_line = [line.strip() for line in output.splitlines() if "SSID" in line]
            ssid = ssid_line[0].split(":")[1].strip()
            return ssid, "Wi-Fi"
        except:
            return "Not connected", "Not supported"

    def get_wifi_info_linux(self):
        try:
            import pydbus
            bus = pydbus.SystemBus()
            network_manager = bus.get("org.freedesktop.NetworkManager")
            active_connections = network_manager.Get("org.freedesktop.NetworkManager", "ActiveConnections")
            for connection in active_connections:
                properties = network_manager.Get("org.freedesktop.NetworkManager.Connection.Active", connection, "Ssid")
                if properties:
                    ssid = properties
                    return ssid, "Wi-Fi"
            return "Not connected", "Not supported"
        except:
            return "Not connected", "Not supported"

    def get_gpu_info(self):
        system = platform.system()
        if system == "Windows":
            return self.get_gpu_info_windows()
        elif system == "Linux":
            return self.get_gpu_info_linux()
        else:
            return "Not supported", "Not supported"

    def get_gpu_info_windows(self):
        try:
            import subprocess
            output = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu,name", "--format=csv,noheader,nounits"]).decode("utf-8")
            gpu_info = output.strip()
            gpu_info_parts = gpu_info.split(', ')
            return f"{gpu_info_parts[0]}%", gpu_info_parts[1]
        except:
            return "No NVIDIA GPU found", "No NVIDIA GPU found"

    def get_gpu_info_linux(self):
        try:
            import subprocess
            output = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu,name", "--format=csv,noheader,nounits"]).decode("utf-8")
            gpu_info = output.strip()
            gpu_info_parts = gpu_info.split(', ')
            return f"{gpu_info_parts[0]}%", gpu_info_parts[1]
        except:
            return "No NVIDIA GPU found", "No NVIDIA GPU found"
def main():
   
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    performance_window = PerformanceReplica()
    task_manager_window = TaskManagerUI()

    show_performance_button = QPushButton("Show Performance", main_window)
    show_performance_button.setGeometry(20, 20, 150, 30)
    show_performance_button.clicked.connect(performance_window.show)

    show_task_manager_button = QPushButton("Show Task Manager", main_window)
    show_task_manager_button.setGeometry(180, 20, 150, 30)
    show_task_manager_button.clicked.connect(task_manager_window.show)

    main_window.setGeometry(100, 100, 400, 100)
    main_window.setWindowTitle("Main Window")
    main_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
