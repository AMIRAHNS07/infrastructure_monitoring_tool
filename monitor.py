import os
import psutil
import platform
from datetime import datetime

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
    return usage.percent

def check_memory():
    mem = psutil.virtual_memory()
    log(f"Memory Usage: {mem.percent}% used ({mem.used // (1024**2)} MB of {mem.total // (1024**2)} MB)")
    return mem.percent

def check_cpu():
    cpu = psutil.cpu_percent(interval=1)
    log(f"CPU Usage: {cpu}%")
    return cpu

def check_services(services):
    for service in services:
        status = "running" if psutil.win_service_get(service).status() == 'running' else "stopped"
        log(f"Service: {service} - Status: {status}")

if __name__ == "__main__":
    log("---- SYSTEM MONITOR START ----")
    disk = check_disk()
    memory = check_memory()
    cpu = check_cpu()

    if platform.system() == "Windows":
        check_services(["Spooler", "W32Time"])  # Example Windows services
    elif platform.system() == "Linux":
        # For Linux, just check using systemctl
        for service in ["ssh", "cron", "mysql"]:
            status = os.system(f"systemctl is-active --quiet {service}")
            log(f"Service: {service} - Status: {'running' if status == 0 else 'stopped'}")

    log("---- SYSTEM MONITOR END ----\n")
