import platform
import socket
from datetime import datetime

import psutil


class HardwareInfo:
    def get_cpu_info(self):
        cpu_frequency = psutil.cpu_freq()

        if cpu_frequency:
            current_speed = f"{cpu_frequency.current / 1000:.2f} GHz"
            max_speed = f"{cpu_frequency.max / 1000:.2f} GHz"
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
        adapter_addresses = psutil.net_if_addrs()
        adapter_status = psutil.net_if_stats()

        for adapter_name, addresses in adapter_addresses.items():
            ipv4_addresses = []

            for address in addresses:
                if address.family == socket.AF_INET:
                    ipv4_addresses.append(address.address)

            status = adapter_status.get(adapter_name)
            is_up = status.isup if status else False
            speed = status.speed if status else 0

            adapters.append({
                "name": adapter_name,
                "ipv4": ", ".join(ipv4_addresses) or "No IPv4 address",
                "status": "Connected" if is_up else "Disconnected",
                "speed_mbps": speed,
            })

        return adapters

    def get_system_info(self):
        boot_timestamp = psutil.boot_time()
        boot_time = datetime.fromtimestamp(boot_timestamp)

        return {
            "computer_name": platform.node(),
            "operating_system": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "python_version": platform.python_version(),
            "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def get_all_info(self):
        return {
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disks": self.get_disk_info(),
            "network": self.get_network_info(),
            "system": self.get_system_info(),
        }
