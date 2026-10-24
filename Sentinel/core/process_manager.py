import psutil


class ProcessManager:

    def get_processes(self):
        processes = []

        for process in psutil.process_iter(
            ["pid", "name", "username", "memory_info", "status"]
        ):
            try:
                info = process.info
                memory_info = info.get("memory_info")

                memory_mb = (
                    memory_info.rss / (1024 ** 2)
                    if memory_info else 0
                )

                # Read CPU usage without waiting for every process
                cpu_percent = process.cpu_percent(interval=None)

                processes.append({
                    "pid": info.get("pid", 0),
                    "name": info.get("name") or "Unknown",
                    "username": info.get("username") or "Unknown",
                    "memory_mb": memory_mb,
                    "cpu_percent": cpu_percent,
                    "status": info.get("status") or "Unknown"
                })

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):
                # A process may close or become inaccessible during scanning
                continue

        return processes

    def terminate_process(self, pid):
        try:
            process = psutil.Process(pid)

            # Request termination; Windows may deny access to protected processes
            process.terminate()

            return True, f"Termination requested for PID {pid}."

        except psutil.NoSuchProcess:
            return False, "This process is no longer running."

        except psutil.AccessDenied:
            return False, "Access denied. This process may require administrator permissions."

        except psutil.Error as error:
            return False, f"Unable to terminate process: {error}"
