import platform
import socket
import time
from datetime import datetime, timedelta

import psutil


class HardwareInfo:
    def get_cpu_info(self):
        frequency = psutil.cpu_freq()

        if frequency:
            current_speed = f"{frequency.current / 1000:.2f} GHz"
            max_speed = (
                f"{frequency.max / 1000:.2f} GHz"
                if frequency.max
                else "Not available"
            )
        else:
            current_speed = "Not available"
            max_speed = "Not available"

        return {
            "processor": platform.processor() or "Not available",
            "architecture": platform.machine(),
            "physical_cores": psutil.cpu_count(logical=False) or 0,
            "logical_cores": psutil.cpu_count(logical=True) or 0,
            "current_speed": current_speed,
            "max_speed": max_speed,
            "usage_percent": psutil.cpu_percent(interval=None),
        }

    def get_memory_info(self):
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return {
            "total_gb": round(memory.total / (1024 ** 3), 2),
            "used_gb": round(memory.used / (1024 ** 3), 2),
            "available_gb": round(memory.available / (1024 ** 3), 2),
            "usage_percent": memory.percent,
            "swap_total_gb": round(swap.total / (1024 ** 3), 2),
            "swap_used_gb": round(swap.used / (1024 ** 3), 2),
            "swap_percent": swap.percent,
        }

    def get_disk_info(self):
        drives = []

        for partition in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(partition.mountpoint)

                drives.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "filesystem": partition.fstype or "Unknown",
                    "total_gb": round(usage.total / (1024 ** 3), 2),
                    "used_gb": round(usage.used / (1024 ** 3), 2),
                    "free_gb": round(usage.free / (1024 ** 3), 2),
                    "usage_percent": usage.percent,
                })

            except (PermissionError, OSError):
                continue

        return drives

    def get_network_info(self):
        adapters = []
        addresses = psutil.net_if_addrs()
        statuses = psutil.net_if_stats()
        counters = psutil.net_io_counters(pernic=True)

        for name, adapter_addresses in addresses.items():
            ipv4 = []
            ipv6 = []

            for address in adapter_addresses:
                if address.family == socket.AF_INET:
                    ipv4.append(address.address)
                elif address.family == socket.AF_INET6:
                    ipv6.append(address.address.split("%")[0])

            status = statuses.get(name)
            counter = counters.get(name)

            adapters.append({
                "name": name,
                "ipv4": ", ".join(ipv4) or "Not available",
                "ipv6": ", ".join(ipv6) or "Not available",
                "status": (
                    "Connected" if status and status.isup
                    else "Disconnected"
                ),
                "speed_mbps": status.speed if status else 0,
                "bytes_sent_mb": (
                    round(counter.bytes_sent / (1024 ** 2), 2)
                    if counter else 0
                ),
                "bytes_received_mb": (
                    round(counter.bytes_recv / (1024 ** 2), 2)
                    if counter else 0
                ),
            })

        return adapters

    def get_battery_info(self):
        try:
            battery = psutil.sensors_battery()
        except (AttributeError, OSError):
            battery = None

        if battery is None:
            return {
                "available": False,
                "message": "Battery information is unavailable.",
            }

        if battery.power_plugged:
            power_status = "Plugged in"
        else:
            power_status = "On battery"

        if battery.secsleft == psutil.POWER_TIME_UNLIMITED:
            remaining = "Unlimited"
        elif battery.secsleft == psutil.POWER_TIME_UNKNOWN:
            remaining = "Unknown"
        else:
            remaining = str(
                timedelta(seconds=max(0, battery.secsleft))
            )

        return {
            "available": True,
            "percent": battery.percent,
            "power_status": power_status,
            "time_remaining": remaining,
        }

    def get_temperature_info(self):
        # Temperature sensor support varies by operating system and hardware.
        try:
            sensors = psutil.sensors_temperatures(fahrenheit=False)
        except (AttributeError, OSError):
            sensors = {}

        readings = []

        for sensor_name, entries in sensors.items():
            for entry in entries:
                readings.append({
                    "sensor": sensor_name,
                    "label": entry.label or "Unnamed sensor",
                    "current_celsius": entry.current,
                    "high_celsius": entry.high,
                    "critical_celsius": entry.critical,
                })

        return {
            "available": bool(readings),
            "readings": readings,
            "message": (
                "Temperature sensors detected."
                if readings
                else "Temperature readings are not exposed by this system."
            ),
        }

    def get_system_info(self):
        boot_timestamp = psutil.boot_time()
        boot_time = datetime.fromtimestamp(boot_timestamp)
        uptime_seconds = max(0, time.time() - boot_timestamp)

        return {
            "computer_name": platform.node(),
            "operating_system": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "architecture": platform.architecture()[0],
            "python_version": platform.python_version(),
            "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
            "uptime": str(timedelta(seconds=int(uptime_seconds))),
        }

    def get_all_info(self):
        return {
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disks": self.get_disk_info(),
            "network": self.get_network_info(),
            "battery": self.get_battery_info(),
            "temperature": self.get_temperature_info(),
            "system": self.get_system_info(),
        }
