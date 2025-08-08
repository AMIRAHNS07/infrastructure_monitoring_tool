# infrastructure_monitoring_tool

A lightweight Python script that monitors system health: disk usage, memory, CPU, and running services. Logs results and can send alerts if thresholds are breached.

## ✅ Features
- Cross-platform: Linux & Windows
- Checks disk, CPU, RAM usage
- Logs to a daily `.log` file
- Verifies key service status
- Easy to extend with alerts/email

## 🚀 Setup
```bash
pip install -r requirements.txt
python monitor.py
