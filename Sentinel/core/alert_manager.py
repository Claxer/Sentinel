from datetime import datetime


class AlertManager:
    def __init__(
        self,
        cpu_limit=85,
        ram_limit=85,
        disk_limit=90
    ):
        self.cpu_limit = cpu_limit
        self.ram_limit = ram_limit
        self.disk_limit = disk_limit

        self.active_alerts = {}
        self.alert_history = []
        self.max_history = 200

    def check_metrics(self, metrics):
        current_alerts = {}

        checks = [
            (
                "high_cpu",
                "High CPU Usage",
                metrics.get("cpu", 0),
                self.cpu_limit,
                "CPU usage is above the configured limit."
            ),
            (
                "high_ram",
                "High Memory Usage",
                metrics.get("ram", 0),
                self.ram_limit,
                "RAM usage is above the configured limit."
            ),
            (
                "high_disk",
                "High Disk Usage",
                metrics.get("disk", 0),
                self.disk_limit,
                "Disk usage is above the configured limit."
            )
        ]

        for alert_id, title, value, limit, description in checks:
            if value >= limit:
                current_alerts[alert_id] = {
                    "id": alert_id,
                    "title": title,
                    "description": description,
                    "value": round(value, 1),
                    "limit": limit,
                    "severity": (
                        "Critical" if value >= 95 else "Warning"
                    ),
                    "timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "status": "Active"
                }

        for alert_id, alert in current_alerts.items():
            if alert_id not in self.active_alerts:
                self.alert_history.insert(0, alert.copy())
                self.alert_history = self.alert_history[
                    :self.max_history
                ]

        self.active_alerts = current_alerts

        return self.get_active_alerts()

    def get_active_alerts(self):
        return list(self.active_alerts.values())

    def get_alert_history(self):
        return list(self.alert_history)

    def clear_history(self):
        self.alert_history.clear()

    def update_thresholds(
        self,
        cpu_limit=None,
        ram_limit=None,
        disk_limit=None
    ):
        if cpu_limit is not None:
            self.cpu_limit = max(1, min(100, cpu_limit))

        if ram_limit is not None:
            self.ram_limit = max(1, min(100, ram_limit))

        if disk_limit is not None:
            self.disk_limit = max(1, min(100, disk_limit))

    def get_thresholds(self):
        return {
            "cpu": self.cpu_limit,
            "ram": self.ram_limit,
            "disk": self.disk_limit
        }
