import os
import psutil


class ProcessManager:
    """Collect process information and safely request process termination."""

    def __init__(self):
        self.current_pid = os.getpid()

    def get_processes(self):
        """Return accessible running processes, sorted by CPU usage."""
        processes = []

        try:
            iterator = psutil.process_iter(
                ["pid", "name", "username", "memory_info", "cpu_percent", "status"]
            )

            for process in iterator:
                try:
                    info = process.info
                    pid = info.get("pid")

                    if pid is None:
                        continue

                    memory_info = info.get("memory_info")
                    memory_mb = (
                        round(memory_info.rss / (1024 * 1024), 2)
                        if memory_info else 0.0
                    )

                    processes.append({
                        "pid": int(pid),
                        "name": info.get("name") or "Unknown",
                        "username": info.get("username") or "Unavailable",
                        "memory": memory_mb,
                        "memory_mb": memory_mb,
                        "cpu": round(float(info.get("cpu_percent") or 0.0), 1),
                        "cpu_percent": round(float(info.get("cpu_percent") or 0.0), 1),
                        "status": info.get("status") or "Unknown",
                    })

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                    OSError,
                    TypeError,
                    ValueError,
                ):
                    continue

        except (psutil.Error, OSError):
            return []

        processes.sort(key=lambda item: item["cpu"], reverse=True)
        return processes

    def get_process_details(self, pid):
        """Return a consistent success/message/process result."""
        try:
            pid = int(pid)

            if pid <= 0:
                return {
                    "success": False,
                    "message": "Please select a valid process ID.",
                    "process": None,
                }

            process = psutil.Process(pid)
            with process.oneshot():
                memory_info = process.memory_info()
                details = {
                    "pid": process.pid,
                    "name": process.name(),
                    "username": self._safe_call(process.username),
                    "status": self._safe_call(process.status),
                    "cpu": round(float(self._safe_call(process.cpu_percent) or 0.0), 1),
                    "memory": round(memory_info.rss / (1024 * 1024), 2),
                    "memory_mb": round(memory_info.rss / (1024 * 1024), 2),
                    "created": self._safe_call(process.create_time),
                    "executable": self._safe_call(process.exe),
                    "command_line": self._safe_call(process.cmdline),
                }

            return {
                "success": True,
                "message": "Process details retrieved successfully.",
                "process": details,
            }

        except (ValueError, TypeError):
            return {
                "success": False,
                "message": "The process ID must be a valid number.",
                "process": None,
            }
        except psutil.NoSuchProcess:
            return {
                "success": False,
                "message": "The process no longer exists.",
                "process": None,
            }
        except psutil.AccessDenied:
            return {
                "success": False,
                "message": "Windows denied access to this process.",
                "process": None,
            }
        except (psutil.Error, OSError) as error:
            return {
                "success": False,
                "message": f"Could not retrieve process details: {error}",
                "process": None,
            }

    def terminate_process(self, pid):
        """Request process termination, waiting up to three seconds.

        This method intentionally does not force-kill a process after timeout.
        """
        try:
            pid = int(pid)

            if pid <= 0:
                return {"success": False, "message": "Please select a valid process ID."}

            if pid == self.current_pid:
                return {
                    "success": False,
                    "message": "Sentinel cannot terminate its own process.",
                }

            process = psutil.Process(pid)

            if not process.is_running():
                return {"success": False, "message": "This process is no longer running."}

            process.terminate()

            try:
                process.wait(timeout=3)
                return {
                    "success": True,
                    "message": f"Process {pid} was terminated successfully.",
                }
            except psutil.TimeoutExpired:
                return {
                    "success": False,
                    "message": (
                        f"Process {pid} did not exit within three seconds. "
                        "It was not force-killed."
                    ),
                }

        except (ValueError, TypeError):
            return {"success": False, "message": "The process ID must be a valid number."}
        except psutil.NoSuchProcess:
            return {"success": False, "message": "The process no longer exists."}
        except psutil.AccessDenied:
            return {
                "success": False,
                "message": "Windows denied permission to terminate this process.",
            }
        except (psutil.Error, OSError) as error:
            return {"success": False, "message": f"Could not terminate process: {error}"}

    @staticmethod
    def _safe_call(function):
        """Call a process method without allowing optional details to break the result."""
        try:
            return function()
        except (psutil.Error, OSError):
            return "Unavailable"
