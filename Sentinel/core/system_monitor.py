import os
import platform
import time
from datetime import timedelta

import psutil


class SystemMonitor:

    def __init__(self):
        self.previous_sent = psutil.net_io_counters().bytes_sent
        self.previous_received = psutil.net_io_counters().bytes_recv
        self.last_network_check = time.time()

        # Initialize CPU measurement
        psutil.cpu_percent(interval=None)

    @staticmethod
    def format_speed(bytes_per_second):
        if bytes_per_second >= 1024 ** 2:
            return f"{bytes_per_second / (1024 ** 2):.2f} MB/s"

        return f"{bytes_per_second / 1024:.1f} KB/s"

    def get_metrics(self):
        cpu = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(os.path.abspath(os.sep))

        network = psutil.net_io_counters()
        current_time = time.time()
        elapsed = max(current_time - self.last_network_check, 0.001)

        upload_speed = max(
            0,
            network.bytes_sent - self.previous_sent
        ) / elapsed

        download_speed = max(
            0,
            network.bytes_recv - self.previous_received
        ) / elapsed

        self.previous_sent = network.bytes_sent
        self.previous_received = network.bytes_recv
        self.last_network_check = current_time

        uptime_seconds = time.time() - psutil.boot_time()

        return {
            "cpu": cpu,
            "ram": memory.percent,
            "ram_used_gb": memory.used / (1024 ** 3),
            "ram_total_gb": memory.total / (1024 ** 3),
            "disk": disk.percent,
            "disk_used_gb": disk.used / (1024 ** 3),
            "disk_total_gb": disk.total / (1024 ** 3),
            "upload_speed": upload_speed,
            "download_speed": download_speed,
            "uptime": str(timedelta(seconds=int(uptime_seconds))),
            "computer": platform.node(),
            "os": f"{platform.system()} {platform.release()}",
            "processor": platform.processor() or "Not available",
            "physical_cores": psutil.cpu_count(logical=False) or 0,
            "logical_cores": psutil.cpu_count(logical=True) or 0,
        }
