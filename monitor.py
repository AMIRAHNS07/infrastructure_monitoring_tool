import psutil
import smtplib
import argparse
import json
import platform
import socket
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def send_email_alert_html(subject, html_body, config):
    msg = MIMEMultipart("alternative")
    msg["From"] = config["email_alerts"]["sender_email"]
    msg["To"] = config["email_alerts"]["receiver_email"]
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(config["email_alerts"]["smtp_server"], config["email_alerts"]["smtp_port"]) as server:
        server.starttls()
        server.login(config["email_alerts"]["username"], config["email_alerts"]["password"])
        server.send_message(msg)

def get_system_info():
    os_name = f"{platform.system()} {platform.release()}"
    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except:
        ip_address = "Unavailable"
    python_ver = platform.python_version()
    cpu_cores = psutil.cpu_count(logical=True)
    total_ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    return os_name, hostname, ip_address, python_ver, cpu_cores, total_ram_gb

def check_metrics(config):
    alerts = []
    html_rows = ""
    thresholds = config["thresholds"]

    # CPU
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_color = "red" if cpu_usage > thresholds["cpu"] else "green"
    if cpu_usage > thresholds["cpu"]:
        alerts.append(f"High CPU usage: {cpu_usage}%")
    html_rows += f"<tr><td><b>CPU Usage</b></td><td style='color:{cpu_color};'>{cpu_usage}%</td><td>{thresholds['cpu']}%</td></tr>"

    # Memory
    mem_usage = psutil.virtual_memory().percent
    mem_color = "red" if mem_usage > thresholds["memory"] else "green"
    if mem_usage > thresholds["memory"]:
        alerts.append(f"High Memory usage: {mem_usage}%")
    html_rows += f"<tr><td><b>Memory Usage</b></td><td style='color:{mem_color};'>{mem_usage}%</td><td>{thresholds['memory']}%</td></tr>"

    # Disk
    disk_usage = psutil.disk_usage("/").percent
    disk_color = "red" if disk_usage > thresholds["disk"] else "green"
    if disk_usage > thresholds["disk"]:
        alerts.append(f"High Disk usage: {disk_usage}%")
    html_rows += f"<tr><td><b>Disk Usage</b></td><td style='color:{disk_color};'>{disk_usage}%</td><td>{thresholds['disk']}%</td></tr>"

    return alerts, html_rows, cpu_usage, mem_usage, disk_usage

def check_services(config):
    html_service_rows = ""
    service_statuses = {}
    os_type = platform.system().lower()

    if os_type in config["services"]:
        for service in config["services"][os_type]:
            try:
                if os_type == "windows":
                    service_running = any(
                        svc.name().lower() == service.lower() and svc.status() == 'running'
                        for svc in psutil.win_service_iter()
                    )
                else:
                    service_running = None
                status = "Running" if service_running else "Not Running"
                color = "green" if service_running else "red"
                service_statuses[service] = status
            except Exception:
                status = "Not Found"
                color = "gray"
                service_statuses[service] = status

            html_service_rows += f"<tr><td>{service}</td><td style='color:{color};'><b>{status}</b></td></tr>"

    return html_service_rows, service_statuses

def log_to_file(timestamp, cpu, mem, disk, services, alerts):
    """Append monitoring results to logs.txt"""
    with open("logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] ---- SYSTEM MONITOR START ----\n")
        log_file.write(f"[{timestamp}] CPU Usage: {cpu:.2f}%\n")
        log_file.write(f"[{timestamp}] Memory Usage: {mem:.2f}%\n")
        log_file.write(f"[{timestamp}] Disk Usage: {disk:.2f}%\n")
        for svc, status in services.items():
            log_file.write(f"[{timestamp}] Service: {svc} - Status: {status}\n")
        if alerts:
            log_file.write(f"[{timestamp}] ALERTS:\n")
            for alert in alerts:
                log_file.write(f"[{timestamp}] ⚠ {alert}\n")
        log_file.write(f"[{timestamp}] ---- SYSTEM MONITOR END ----\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["email", "console"], default="console")
    args = parser.parse_args()

    config = load_config()

    alerts, html_metrics, cpu_usage, mem_usage, disk_usage = check_metrics(config)
    html_services, service_statuses = check_services(config)
    os_name, hostname, ip_address, python_ver, cpu_cores, total_ram_gb = get_system_info()

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[LOG] {now_str} | CPU: {cpu_usage:.2f}% | Memory: {mem_usage:.2f}% | Disk: {disk_usage:.2f}%")

    # Log locally every time
    log_to_file(now_str, cpu_usage, mem_usage, disk_usage, service_statuses, alerts)

    if args.mode == "email" and config["email_alerts"]["enabled"]:
        if alerts:
            subject = f"🚨 System Monitoring Alert - {platform.system()} - {now_str}"
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color:#d9534f;">🚨 System Monitoring Alert</h2>
                <p>Report generated at {now_str}</p>
                <h3>📊 System Health</h3>
                <table border="1" cellpadding="5" cellspacing="0">
                    <tr><th>Metric</th><th>Current</th><th>Threshold</th></tr>
                    {html_metrics}
                </table>
                <h3>🛠 Service Status</h3>
                <table border="1" cellpadding="5" cellspacing="0">
                    <tr><th>Service</th><th>Status</th></tr>
                    {html_services}
                </table>
                <h3>📋 System Information</h3>
                <table border="1" cellpadding="5" cellspacing="0">
                    <tr><td>OS</td><td>{os_name}</td></tr>
                    <tr><td>Hostname</td><td>{hostname}</td></tr>
                    <tr><td>IP Address</td><td>{ip_address}</td></tr>
                    <tr><td>Python Version</td><td>{python_ver}</td></tr>
                    <tr><td>CPU Cores</td><td>{cpu_cores}</td></tr>
                    <tr><td>Total RAM</td><td>{total_ram_gb} GB</td></tr>
                </table>
                <p style="margin-top:20px; font-size:12px; color:gray;">
                    This is an automated alert from the Infrastructure Monitoring Tool. Please investigate if any metrics are in <b style="color:red;">red</b>.
                </p>
            </body>
            </html>
            """
            send_email_alert_html(subject, html_body, config)
            print("[INFO] Alert sent due to high usage.")
        else:
            print("[INFO] System within safe limits. No alert sent.")
    else:
        if alerts:
            print("[INFO] System is at risk:")
            for alert in alerts:
                print(f" - {alert}")
        else:
            print("[INFO] System within safe limits.")
