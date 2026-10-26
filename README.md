# Sentinel — System Monitoring and Management Tool

Sentinel is a Python-based desktop application designed to monitor system performance, view and manage running processes, display hardware information, detect potential system resource issues, and export useful system reports. It features a professional dark interface using charcoal, black, and grey colors, inspired by modern system management dashboards.

The project is being developed using **Python, PyCharm, CustomTkinter, psutil, and Matplotlib** on Windows 11.

## Project Overview

Sentinel provides a centralized dashboard for monitoring computer performance, viewing hardware specifications, managing running processes, identifying potential system resource issues, and exporting monitoring data into CSV reports.

The application includes five main modules:

1. **Dashboard** — Monitor CPU, memory, disk, and network activity through live statistics and performance graphs.
2. **Processes** — View running processes, search by process name or PID, inspect resource usage, and request process termination.
3. **Hardware Information** — Display processor specifications, memory information, storage drives, network adapters, battery status, temperature readings where supported, and operating system details.
4. **Alerts** — Detect high CPU usage, high memory usage, and high disk usage based on configured thresholds.
5. **Reports** — Generate and export system metrics, running process information, active alerts, and alert history as CSV files.

## Current Development Progress

Sentinel is developed in stages, starting with core monitoring components and integrating additional functionality into the desktop interface.

### Implemented Features

- **Project Foundation** — Established the main application entry point and modular project structure.
- **System Monitoring** — Collect CPU usage, RAM usage, disk usage, network transfer speeds, computer information, and system uptime using `psutil`.
- **Live Performance Graphs** — Display CPU and RAM usage alongside network download activity using Matplotlib.
- **Automatic Dashboard Updates** — Refresh system metrics and graphs periodically.
- **Process Manager** — Display running processes with their PID, name, CPU usage, memory usage, user, and status.
- **Process Search** — Search for processes by name or process ID.
- **Process Termination** — Request termination of a selected process after user confirmation, subject to operating system permissions.
- **Automatic Process Refresh** — Refresh the process list periodically.
- **Hardware Information** — Collect processor details, physical and logical cores, CPU frequency where available, RAM and swap usage, storage capacity, network adapter details, and system information.
- **Battery Information** — Retrieve battery percentage, power connection status, and estimated remaining time when supported.
- **Temperature Information** — Attempt to retrieve hardware temperature readings when the operating system and hardware expose them through `psutil`.
- **Network Adapter Details** — Display adapter status, available IPv4 addresses, reported link speed, and cumulative sent and received data.
- **Alert Manager** — Monitor CPU, RAM, and disk usage against configurable thresholds.
- **Alert Severity** — Classify resource alerts as Warning or Critical according to configured limits and current readings.
- **Active Alerts** — Display currently triggered resource alerts.
- **Alert History** — Record newly triggered alert events in memory, with a maximum of 200 entries.
- **System Metrics Report** — Export current system metrics, including available CPU, memory, disk, network, and other monitoring information.
- **Process Report** — Export information about currently running processes.
- **Active Alerts Report** — Export alerts that are currently active.
- **Alert History Report** — Export alert events recorded during the current application session.
- **CSV Export** — Save reports as `.csv` files that can be opened in spreadsheet applications.
- **Save Location Selection** — Choose the destination and filename for exported reports through a save-file dialog.
- **Export Feedback** — Display success or error messages when exporting reports.
- **Shared Monitoring Integration** — Connect the Dashboard and Alerts page to the system monitoring and alert management components.
- **Main Application Navigation** — Provide navigation for Dashboard, Processes, Hardware, Alerts, and Reports.
- **Dark Interface** — Use a consistent dark-themed desktop layout with charcoal, black, and grey colors.

### Current Limitations

- Alert history is stored in memory and is cleared when the application closes.
- Reports contain a snapshot of the information available when the export is requested; continuous historical metric recording is not yet implemented.
- Hardware temperature readings depend on available sensor support and may not appear on some Windows computers.
- Battery information is unavailable on systems without a supported battery interface.
- CPU frequency and network link speed may not be reported on every system.
- Process termination may fail when administrator permissions are required or the operating system prevents access.
- Storage usage information does not currently provide a complete SSD or HDD health assessment.
- The application is still under development, and further testing and performance improvements are planned.

## Technologies Used

- **Python** — Main programming language.
- **CustomTkinter** — Modern desktop graphical user interface.
- **psutil** — System resource, process, network, disk, and battery information.
- **Matplotlib** — Live performance graphs and data visualization.
- **Tkinter and ttk** — Native interface components, process tables, scrollbars, file dialogs, and confirmation messages.
- **CSV module** — Export monitoring information into comma-separated value files.
- **PyCharm** — Development environment.
- **Windows 11** — Primary development platform.

## Project Structure

The project separates monitoring logic, interface components, and supporting utilities to make the application easier to maintain and expand.

```text
Sentinel/
├── main.py
├── requirements.txt
├── README.md
│
├── core/
│   ├── __init__.py
│   ├── system_monitor.py
│   ├── process_manager.py
│   ├── hardware_info.py
│   ├── alert_manager.py
│   └── report_manager.py
│
├── ui/
│   ├── __init__.py
│   ├── hardware.py
│   ├── alerts.py
│   └── reports.py
│
├── database/
│   ├── __init__.py
│   └── db_manager.py
│
├── utils/
│   ├── __init__.py
│   ├── export_manager.py
│   └── helpers.py
│
└── assets/
    └── icons/
```

**Note:** This is an overview of the project structure, including folders reserved for future development. In the current implementation, the Dashboard and Process Manager are integrated directly into `main.py`, while Hardware, Alerts, and Reports use separate interface modules. Some listed database and utility files may not exist yet.

## Installation

### 1. Install Python

Install Python for Windows if it is not already available. Make sure Python is accessible from your terminal.

### 2. Open the Project

Open the Sentinel project folder in PyCharm.

### 3. Install Dependencies

Open the PyCharm terminal in the project directory and run:

```bash
python -m pip install -r requirements.txt
```

Make sure `requirements.txt` includes:

```text
customtkinter
psutil
matplotlib
```

The CSV functionality uses Python's built-in `csv` module, so an additional package is not required.

### 4. Run Sentinel

From the project's root directory, run:

```bash
python main.py
```

The main window should open with navigation for Dashboard, Processes, Hardware, Alerts, and Reports.

## Module Details

### Dashboard

The Dashboard provides an overview of current system performance.

- CPU utilization.
- RAM utilization and memory capacity.
- Disk utilization and storage capacity.
- Network upload and download speeds.
- Computer name and operating system.
- Processor information.
- System uptime.
- CPU and RAM performance graphs.
- Network download activity graph.
- Periodic metric refreshes.
- Automatic resource alert checks.

### Process Manager

The Process Manager provides a searchable view of running processes.

- Process ID and name.
- CPU usage and memory consumption.
- Username and process status.
- Search by process name or PID.
- Periodic process list refresh.
- Selected-process termination with confirmation.
- Error handling for inaccessible or terminated processes.

Process termination is subject to operating system permissions and should be used carefully. Ending essential system processes may cause instability.

### Hardware Information

The Hardware module presents information collected by `core/hardware_info.py`.

- Processor model and architecture.
- Physical and logical processor cores.
- Current and maximum reported CPU frequency.
- RAM capacity, usage, and availability.
- Swap memory usage.
- Accessible disk partitions and storage utilization.
- Network adapter addresses and connection status.
- Cumulative network data transferred per adapter.
- Battery status where available.
- Hardware temperature readings where supported.
- Operating system version.
- Python version, boot time, and uptime.

### Alerts

The Alerts module uses `core/alert_manager.py` to evaluate monitored system metrics.

Default thresholds:

| Resource | Default threshold |
|---|---:|
| CPU usage | 85% |
| RAM usage | 85% |
| Disk usage | 90% |

Readings at or above 95% are classified as Critical.

The module includes:

- Active alert summaries.
- Alert severity indicators.
- Alert timestamps and descriptions.
- Configurable resource thresholds through the `AlertManager` class.
- An in-memory history of newly triggered alert events.
- A maximum alert history of 200 entries.

Alert history is session-based and is not retained after Sentinel closes.

### Reports

The Reports module allows users to export useful monitoring information without manually copying data from the application.

#### Available Reports

**1. System Metrics Report**

Exports the system metrics currently returned by `SystemMonitor`, such as CPU usage, RAM usage, disk usage, network speeds, computer information, and uptime when those values are available.

**2. Process Report**

Exports the current process list returned by `ProcessManager`. Depending on the process information provided by the system, the report can include process IDs, names, usernames, memory usage, CPU usage, and process status.

**3. Active Alerts Report**

Exports alerts that are active at the time of the request, including their timestamps, titles, descriptions, severity, measured values, configured limits, and status.

**4. Alert History Report**

Exports alert events recorded by Sentinel during the current application session. The report can include previously triggered alerts even if they are no longer active.

#### Export Features

- Export reports in CSV format.
- Choose where to save each report.
- Use automatically generated filenames containing the report type and timestamp.
- Open exported files using spreadsheet applications such as Microsoft Excel or compatible software.
- Receive confirmation messages after successful exports.
- Receive error messages if an export fails.

#### Important Reporting Notes

- Reports are snapshots, not live documents.
- System metrics and process information reflect the data collected when the report is generated.
- Alert history is stored in memory and is lost when the application closes.
- If no alerts or processes are available, the report records an appropriate empty-state message.
- Database-backed report storage and long-term historical analysis remain potential future improvements.

### Report File Examples

Sentinel generates filenames similar to these:

```text
sentinel_system_20261026_180000.csv
sentinel_processes_20261026_180000.csv
sentinel_active_alerts_20261026_180000.csv
sentinel_alert_history_20261026_180000.csv
```

The actual timestamp depends on when each report is exported.

## Design Goals

- **Clean Interface** — A modern desktop layout with a dark charcoal, black, and grey color palette.
- **Modular Architecture** — Keep monitoring logic separate from interface components where practical.
- **Live Monitoring** — Display regularly refreshed system metrics and performance graphs.
- **Process Management** — Provide process visibility and controlled termination requests.
- **System Diagnostics** — Collect hardware, storage, network, and operating system information.
- **Alert Monitoring** — Identify resource usage that exceeds configured thresholds.
- **Report Generation** — Make monitoring information available as exportable CSV files.
- **Maintainability** — Develop individual modules independently while preserving existing functionality.
- **Extensibility** — Provide a foundation for persistent monitoring history, report generation, and additional diagnostics.

## Development Roadmap

| Stage | Module or Task | Status |
|---|---|---|
| 1 | Project foundation and main application | Implemented |
| 2 | System monitoring and live graphs | Implemented |
| 3 | Process Manager | Implemented |
| 4 | Hardware Information module | Implemented; further refinement planned |
| 5 | Alert Manager and Alerts page | Implemented; further refinement planned |
| 6 | Reports page and CSV exports | Implemented; testing and refinement planned |
| 7 | Database and persistent monitoring history | Planned |
| 8 | Integration testing, performance optimization, and refinement | In progress |

## Project Purpose

Sentinel is a personal software development project focused on building practical programming and IT skills through a modular Python desktop application.

It provides hands-on experience with graphical user interfaces, operating system information, resource monitoring, process management, data visualization, alert logic, CSV file handling, and application architecture.

The project will continue to expand as additional modules are developed, tested, and integrated into the main application.
