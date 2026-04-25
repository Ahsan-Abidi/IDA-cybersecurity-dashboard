import time
from analyzer import analyze_logs

live_data = []

def monitor_logs(file_path):
    global live_data

    while True:
        with open(file_path, "r") as f:
            logs = f.readlines()

        live_data = analyze_logs(logs)
        time.sleep(5)