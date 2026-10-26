import csv
from datetime import datetime


class ReportManager:
    def __init__(self):
        self.report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def export_system_report(self, file_path, metrics):
        """Export current system metrics to a CSV file."""
        with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)

            writer.writerow(["SENTINEL SYSTEM REPORT"])
            writer.writerow(["Report Generated", self.report_time])
            writer.writerow([])
            writer.writerow(["Metric", "Value"])

            for key, value in metrics.items():
                readable_name = key.replace("_", " ").title()
                writer.writerow([readable_name, value])

        return file_path

    def export_process_report(self, file_path, processes):
        """Export the current process list to a CSV file."""
        with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)

            writer.writerow(["SENTINEL PROCESS REPORT"])
            writer.writerow(["Report Generated", self.report_time])
            writer.writerow([])

            if processes:
                headers = list(processes[0].keys())
                writer.writerow(headers)

                for process in processes:
                    writer.writerow([
                        process.get(header, "")
                        for header in headers
                    ])
            else:
                writer.writerow(["No process information available"])

        return file_path

    def export_alert_report(self, file_path, alerts):
        """Export active alerts or alert history to a CSV file."""
        with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)

            writer.writerow(["SENTINEL ALERT REPORT"])
            writer.writerow(["Report Generated", self.report_time])
            writer.writerow([])

            fields = [
                "timestamp",
                "title",
                "description",
                "severity",
                "value",
                "limit",
                "status"
            ]

            writer.writerow(fields)

            for alert in alerts:
                writer.writerow([
                    alert.get(field, "")
                    for field in fields
                ])

        return file_path
