import os
import psutil
import platform
import json
from datetime import datetime

# Load configuration
CONFIG_FILE = "config.json"
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

cpu_threshold = config["thresholds"]["cpu"]
memory_threshold = config["thresholds"]["memory"]
disk_threshold = config["thresholds"]["disk"]
services_linux = config["services"]["linux"]
services_windows = config["services"]["windows"]
email_enabled = config["email_alerts"]["enabled"]

# Create log directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_message = f"{timestamp} {message}"
    print(full_message)
    with open(f"{LOG_DIR}/{datetime.now().strftime('%Y-%m-%d')}-monitor.log", "a") as f:
        f.write(full_message + "\n")

def check_disk():
    usage = psutil.disk_usage('/')
    log(f"Disk Usage: {usage.percent}% used ({usage.used // (1024**3)} GB of {usage.total // (1024**3)} GB)")
    if usage.percent > disk_threshold:
        log(f"ALERT: Disk usage above {disk_threshold}% threshold!")
    return usage.percent

def check_memory():
    mem = psutil.virtual_memory()
    log(f"Memory Usage: {mem.percent}% used ({mem.used // (1024**2)} MB of {mem.total // (1024**2)} MB)")
    if mem.percent > memory_threshold:
        log(f"ALERT: Memory usage above {memory_threshold}% threshold!")
    return mem.percent

def check_cpu():
    cpu = psutil.cpu_percent(interval=1)
    log(f"CPU Usage: {cpu}%")
    if cpu > cpu_threshold:
        log(f"ALERT: CPU usage above {cpu_threshold}% threshold!")
    return cpu

def check_services():
    if platform.system() == "Windows":
        for service in services_windows:
            try:
                status = psutil.win_service_get(service).status()
                log(f"Service: {service} - Status: {status}")
            except Exception:
                log(f"Service: {service} - Status: Not Found")
    elif platform.system() == "Linux":
        for service in services_linux:
            status = os.system(f"systemctl is-active --quiet {service}")
            log(f"Service: {service} - Status: {'running' if status == 0 else 'stopped'}")

if __name__ == "__main__":
    log("---- SYSTEM MONITOR START ----")
    check_disk()
    check_memory()
    check_cpu()
    check_services()
    log("---- SYSTEM MONITOR END ----\n")
