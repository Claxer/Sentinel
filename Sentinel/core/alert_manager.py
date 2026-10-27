import json
from datetime import datetime
from pathlib import Path


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

        self.alert_history = []
        self.active_alerts = []

        self.history_file = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "alert_history.json"
        )

        self.history_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.load_history()

    def check_metrics(self, metrics):
        """Check system metrics and create alerts when limits are reached."""
        limits = {
            "cpu": self.cpu_limit,
            "ram": self.ram_limit,
            "disk": self.disk_limit
        }

        metric_names = {
            "cpu": "CPU Usage",
            "ram": "RAM Usage",
            "disk": "Disk Usage"
        }

        previous_active = {
            alert["metric"]: alert
            for alert in self.active_alerts
        }

        current_active = []

        for metric, limit in limits.items():
            value = metrics.get(metric)

            if value is None:
                continue

            try:
                value = float(value)
            except (TypeError, ValueError):
                continue

            if value >= limit:
                severity = (
                    "Critical" if value >= 95
                    else "Warning"
                )

                alert = {
                    "metric": metric,
                    "name": metric_names[metric],
                    "value": round(value, 2),
                    "threshold": limit,
                    "severity": severity,
                    "message": (
                        f"{metric_names[metric]} is at "
                        f"{value:.1f}% "
                        f"(limit: {limit}%)."
                    ),
                    "timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                }

                current_active.append(alert)

                # Save only newly triggered alerts to history.
                if metric not in previous_active:
                    self.alert_history.append(alert.copy())
                    self._trim_history()
                    self.save_history()

        self.active_alerts = current_active

        return self.active_alerts

    def get_active_alerts(self):
        """Return alerts that are currently active."""
        return [alert.copy() for alert in self.active_alerts]

    def get_alert_history(self):
        """Return saved alert history."""
        return [alert.copy() for alert in self.alert_history]

    def clear_history(self):
        """Clear saved alert history."""
        self.alert_history = []
        return self.save_history()

    def update_thresholds(
        self,
        cpu_limit=None,
        ram_limit=None,
        disk_limit=None
    ):
        """Update alert thresholds."""
        if cpu_limit is not None:
            self.cpu_limit = cpu_limit

        if ram_limit is not None:
            self.ram_limit = ram_limit

        if disk_limit is not None:
            self.disk_limit = disk_limit

    def get_thresholds(self):
        """Return the current alert thresholds."""
        return {
            "cpu_limit": self.cpu_limit,
            "ram_limit": self.ram_limit,
            "disk_limit": self.disk_limit
        }

    def load_history(self):
        """Load previously saved alerts from JSON."""
        if not self.history_file.exists():
            self.alert_history = []
            return self.alert_history

        try:
            with open(
                self.history_file,
                "r",
                encoding="utf-8"
            ) as file:
                saved_history = json.load(file)

            if isinstance(saved_history, list):
                self.alert_history = [
                    item for item in saved_history
                    if isinstance(item, dict)
                ]
            else:
                self.alert_history = []

        except (
            OSError,
            json.JSONDecodeError,
            TypeError
        ):
            self.alert_history = []

        self._trim_history()
        return self.get_alert_history()

    def save_history(self):
        """Save alert history to the JSON file."""
        try:
            self.history_file.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with open(
                self.history_file,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    self.alert_history,
                    file,
                    indent=4
                )

            return True

        except (OSError, TypeError, ValueError) as error:
            print(f"Unable to save alert history: {error}")
            return False

    def _trim_history(self):
        """Keep only the most recent 200 alert events."""
        self.alert_history = self.alert_history[-200:]
