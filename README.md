# infrastructure_monitoring_tool

A Python-based system monitoring and alerting tool that checks CPU, memory, disk usage, and service status. If resource usage exceeds defined thresholds, it sends an email alert.

## ✅ Features
- CPU, Memory, and Disk Usage Monitoring
- Windows Service Status Check (example: Spooler, W32Time)
- Threshold Alerts for CPU, Memory, and Disk
- Email Notifications when thresholds are exceeded
- Detailed System Information included in alert email:
  - OS
  - Python Version
  - CPU Cores
  - Total RAM
 
## 🚀 Requirements
- Python 3.7+
- Install dependencies: pip install psutil

## 🚀 File Structure
- monitor.py # Main monitoring script
-  config.json # Configuration for thresholds, services, and email
-  logs.txt # Log file for monitoring results (auto-generated)

## 🚀 Sample Output (Safe)
[2025-08-08 11:18:34] ---- SYSTEM MONITOR START ----
[2025-08-08 11:18:34] CPU Usage: 1.70%
[2025-08-08 11:18:34] Memory Usage: 55.90%
[2025-08-08 11:18:34] Disk Usage: 62.80%
[2025-08-08 11:18:34] Service: Spooler - Status: Running
[2025-08-08 11:18:34] Service: W32Time - Status: Running
[2025-08-08 11:18:34] ---- SYSTEM MONITOR END ----

## 🚀 Sample Output (Risk)
[2025-08-08 11:04:47] ---- SYSTEM MONITOR START ----
[2025-08-08 11:04:47] CPU Usage: 2.30%
[2025-08-08 11:04:47] Memory Usage: 56.20%
[2025-08-08 11:04:47] Disk Usage: 62.80%
[2025-08-08 11:04:47] Service: Spooler - Status: Running
[2025-08-08 11:04:47] Service: W32Time - Status: Running
[2025-08-08 11:04:47] ALERTS:
[2025-08-08 11:04:47] ⚠ High CPU usage: 2.3%
[2025-08-08 11:04:47] ⚠ High Memory usage: 56.2%
[2025-08-08 11:04:47] ⚠ High Disk usage: 62.8%
[2025-08-08 11:04:47] ---- SYSTEM MONITOR END ----


## 🚀 Setup
```bash
pip install -r requirements.txt
python monitor.py --mode email or python monitor.py --mode console
