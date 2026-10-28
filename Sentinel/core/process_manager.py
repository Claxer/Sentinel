import psutil


class ProcessManager:
    def __init__(self):
        self.process_fields = [
            "pid",
            "name",
            "username",
            "memory_info",
            "cpu_percent",
            "status"
        ]

    def get_processes(self):
        """Return a list of running processes and their resource usage."""
        processes = []

        for process in psutil.process_iter(self.process_fields):
            try:
                info = process.info

                memory_info = info.get("memory_info")
                memory_mb = (
                    round(memory_info.rss / (1024 * 1024), 2)
                    if memory_info
                    else 0.0
                )

                processes.append({
                    "pid": info.get("pid"),
                    "name": info.get("name") or "Unknown",
                    "username": info.get("username") or "Unknown",
                    "memory_mb": memory_mb,
                    "cpu_percent": round(
                        info.get("cpu_percent") or 0.0, 2
                    ),
                    "status": info.get("status") or "Unknown"
                })

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):
                # A process may disappear or become inaccessible.
                continue

            except (OSError, AttributeError, TypeError, ValueError):
                # Skip processes with incomplete or unavailable data.
                continue

        processes.sort(
            key=lambda item: item["cpu_percent"],
            reverse=True
        )

        return processes

    def get_process_details(self, pid):
        """Return detailed information for one process."""
        try:
            pid = int(pid)

            if pid <= 0:
                return {
                    "success": False,
                    "message": "Invalid process ID."
                }

            process = psutil.Process(pid)

            with process.oneshot():
                memory_info = process.memory_info()

                details = {
                    "pid": process.pid,
                    "name": process.name(),
                    "username": self._get_username(process),
                    "cpu_percent": process.cpu_percent(),
                    "memory_mb": round(
                        memory_info.rss / (1024 * 1024), 2
                    ),
                    "status": process.status(),
                    "created": process.create_time()
                }

            return {
                "success": True,
                "message": "Process details retrieved successfully.",
                "process": details
            }

        except ValueError:
            return {
                "success": False,
                "message": "Process ID must be a valid number."
            }

        except psutil.NoSuchProcess:
            return {
                "success": False,
                "message": "The process no longer exists."
            }

        except psutil.AccessDenied:
            return {
                "success": False,
                "message": "Permission denied while reading this process."
            }

        except psutil.ZombieProcess:
            return {
                "success": False,
                "message": "This process is no longer running normally."
            }

        except (OSError, TypeError, AttributeError) as error:
            return {
                "success": False,
                "message": f"Unable to retrieve process details: {error}"
            }

    def terminate_process(self, pid):
        """Safely request termination of a selected process."""
        try:
            pid = int(pid)

            if pid <= 0:
                return {
                    "success": False,
                    "message": "Invalid process ID."
                }

            # Never allow this method to terminate itself.
            if pid == psutil.Process().pid:
                return {
                    "success": False,
                    "message": "Sentinel cannot terminate itself."
                }

            process = psutil.Process(pid)

            # Confirm that the process is still running.
            if not process.is_running():
                return {
                    "success": False,
                    "message": "The process is no longer running."
                }

            process_name = process.name()

            # Request a graceful termination first.
            process.terminate()

            try:
                process.wait(timeout=3)

                return {
                    "success": True,
                    "message": (
                        f"Process '{process_name}' "
                        f"(PID {pid}) was terminated successfully."
                    )
                }

            except psutil.TimeoutExpired:
                return {
                    "success": False,
                    "message": (
                        f"Process '{process_name}' did not exit "
                        "within 3 seconds. It was not force-killed."
                    )
                }

        except ValueError:
            return {
                "success": False,
                "message": "Process ID must be a valid number."
            }

        except psutil.NoSuchProcess:
            return {
                "success": False,
                "message": "The process has already exited."
            }

        except psutil.AccessDenied:
            return {
                "success": False,
                "message": (
                    "Permission denied. You may need administrator "
                    "permissions to terminate this process."
                )
            }

        except psutil.ZombieProcess:
            return {
                "success": False,
                "message": "The process is no longer running normally."
            }

        except (OSError, TypeError, AttributeError) as error:
            return {
                "success": False,
                "message": f"Unable to terminate process: {error}"
            }

    def _get_username(self, process):
        """Retrieve a process username without interrupting monitoring."""
        try:
            return process.username() or "Unknown"
        except (
            psutil.AccessDenied,
            psutil.NoSuchProcess,
            psutil.ZombieProcess
        ):
            return "Unknown"
