# Sentinel — System Monitoring and Management Tool

Sentinel is a Python-based desktop application designed to monitor system performance, view and manage running processes, and organize important computer information in one place. It features a professional dark interface using charcoal, black, and grey colors, inspired by modern system management dashboards.

The project is being developed incrementally using **Python, PyCharm, CustomTkinter, psutil, and Matplotlib** on Windows 11.

## Project Overview

Sentinel aims to provide a centralized dashboard for monitoring computer performance, viewing hardware specifications, managing running processes, and identifying potential system resource issues.

The application is organized into five main modules:

1. **Dashboard** — Monitor CPU, memory, disk, and network activity through live statistics and performance graphs.
2. **Processes** — View running processes, search by process name or PID, inspect resource usage, and request process termination.
3. **Hardware Information** — Display processor specifications, memory information, storage drives, network adapters, battery status, temperature readings where supported, and operating system details.
4. **Alerts** — Detect high CPU usage, high memory usage, and high disk usage based on configurable thresholds.
5. **Reports** — Planned module for organizing monitoring information and exporting reports.

## Current Development Progress

Sentinel is being developed in stages, starting with the core monitoring components before integrating additional functionality into the desktop interface.

### Implemented Features

- **Project Foundation** — Established the main application entry point and modular project structure.
- **System Monitoring** — Collect CPU usage, RAM usage, disk usage, network transfer speeds, computer information, and system uptime using `psutil`.
- **Live Performance Graphs** — Display CPU and RAM usage alongside network upload and download activity using Matplotlib.
- **Automatic Dashboard Updates** — Refresh system metrics and graphs periodically.
- **Process Manager** — Display running processes with their PID, name, CPU usage, memory usage, user, and status.
- **Process Search** — Search for processes by name or process ID.
- **Process Termination** — Request termination of a selected process after user confirmation, subject to operating system permissions.
- **Hardware Information** — Collect processor details, physical and logical cores, CPU frequency where available, RAM and swap usage, storage capacity, network adapter details, and system information.
- **Battery Information** — Retrieve battery percentage, power connection status, and estimated remaining time when supported.
- **Temperature Information** — Attempt to retrieve hardware temperature readings when the operating system and hardware expose them through `psutil`.
- **Network Adapter Details** — Display adapter status, available IPv4 addresses, reported link speed, and cumulative sent and received data.
- **Alert Manager** — Monitor CPU, RAM, and disk usage against configurable thresholds.
- **Alert Severity** — Classify resource alerts as Warning or Critical according to configured limits and current readings.
- **Active Alerts** — Display currently triggered resource alerts.
- **Alert History** — Record newly triggered alert events in memory, with a maximum of 200 entries.
- **Shared Monitoring Integration** — Connect the Dashboard and Alerts page to the system monitoring and alert management components.
- **Main Application Navigation** — Provide navigation for Dashboard, Processes, Hardware, Alerts, and Reports.
- **Dark Interface** — Use a consistent dark-themed desktop layout with charcoal, black, and grey colors.

### Current Limitations

- Alert history is stored in memory and is cleared when the application closes.
- Hardware temperature readings depend on available sensor support and may not appear on some Windows computers.
- Battery information is unavailable on systems without a supported battery interface.
- CPU frequency and network link speed may not be reported on every system.
- Process termination may fail when administrator permissions are required or the operating system prevents access.
- The Reports page is currently a placeholder and does not yet generate or export reports.
- Storage usage information does not currently provide a complete SSD or HDD health assessment.
- The application is still under development, and further testing and performance improvements are planned.

## Technologies Used

- **Python** — Main programming language
- **CustomTkinter** — Modern desktop graphical user interface
- **psutil** — System resource, process, network, disk, and battery information
- **Matplotlib** — Live performance graphs and data visualization
- **Tkinter and ttk** — Native interface components, process tables, scrollbars, and confirmation dialogs
- **PyCharm** — Development environment
- **Windows 11** — Primary development platform

## Project Structure

The project is organized into separate modules to keep system monitoring logic, interface components, and supporting utilities manageable as development continues.

```text
Sentinel/
│
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
│   └── network_monitor.py
│
├── ui/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── processes.py
│   ├── hardware.py
│   ├── alerts.py
│   ├── reports.py
│   └── sidebar.py
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

**Note:** The structure includes planned files that may not exist yet. In the current implementation, the main application integrates the Dashboard and Processes directly in `main.py`, while Hardware and Alerts use separate interface modules. The `network_monitor.py`, database, reporting, and utility modules are reserved for future development unless already created separately.

## Installation

### 1. Install Python

Install Python for Windows if it is not already available. Ensure Python is accessible from the terminal.

### 2. Open the Project

Open the Sentinel project folder in PyCharm.

### 3. Install Dependencies

Open the PyCharm terminal in the project directory and run:

```bash
python -m pip install -r requirements.txt
```

Make sure `requirements.txt` includes the following dependencies:

```text
customtkinter
psutil
matplotlib
```

### 4. Run Sentinel

From the project's root directory, run:

```bash
python main.py
```

The main window should open with navigation for Dashboard, Processes, Hardware, Alerts, and Reports.

## Module Details

### Dashboard

The Dashboard provides an overview of current system performance.

- CPU utilization
- RAM utilization and memory capacity
- Disk utilization and storage capacity
- Network upload and download speeds
- Computer name and operating system
- Processor information and core counts
- System uptime
- CPU and RAM performance graphs
- Network activity graph
- Periodic metric refreshes

### Process Manager

The Process Manager provides a searchable view of running processes.

- Process ID and name
- CPU usage and memory consumption
- Username and process status
- Search by process name or PID
- Periodic process list refresh
- Selected-process termination with confirmation
- Error handling for inaccessible or terminated processes

Process termination is subject to operating system permissions and should be used carefully.

### Hardware Information

The Hardware module presents information collected by `core/hardware_info.py`.

- Processor model and architecture
- Physical and logical processor cores
- Current and maximum reported CPU frequency
- RAM capacity, usage, and availability
- Swap memory usage
- Accessible disk partitions and storage utilization
- Network adapter addresses and connection status
- Cumulative network data transferred per adapter
- Battery status where available
- Hardware temperature readings where supported
- Operating system version, Python version, boot time, and uptime

### Alerts

The Alerts module uses `core/alert_manager.py` to evaluate monitored system metrics.

Default thresholds:

| Resource | Warning threshold |
|---|---:|
| CPU usage | 85% |
| RAM usage | 85% |
| Disk usage | 90% |

Readings at or above 95% are classified as Critical.

The module includes active alert summaries, severity indicators, timestamps, and an in-memory event history. Thresholds can be configured through the `AlertManager` class.

### Reports

The Reports module is planned to provide:

- System performance summaries
- Monitoring history
- Exportable CSV reports
- Resource usage records
- Additional diagnostic summaries

Report generation and exporting are not yet implemented in the current main application.

## Design Goals

- **Clean Interface** — A modern desktop layout with a dark charcoal, black, and grey color palette.
- **Modular Architecture** — Keep monitoring logic separate from interface components where practical.
- **Live Monitoring** — Display regularly refreshed system metrics and performance graphs.
- **Process Management** — Provide process visibility and controlled termination requests.
- **System Diagnostics** — Collect hardware, storage, network, and operating system information.
- **Alert Monitoring** — Identify resource usage that exceeds configured thresholds.
- **Maintainability** — Develop individual modules independently while preserving existing functionality.
- **Extensibility** — Provide a foundation for persistent monitoring history, report generation, and additional diagnostics.

## Development Roadmap

| Stage | Module or Task | Status |
|---|---|---|
| 1 | Project foundation and main application | Completed |
| 2 | System monitoring and live graphs | Implemented |
| 3 | Process Manager | Implemented |
| 4 | Hardware Information module | Implemented; further refinement planned |
| 5 | Alert Manager and Alerts page | Implemented; further refinement planned |
| 6 | Reports and data export | Planned |
| 7 | Database and persistent monitoring history | Planned |
| 8 | Integration testing, performance optimization, and refinement | In progress |

## Project Purpose

Sentinel is a personal software development project focused on building practical programming skills through a modular Python desktop application.

It provides hands-on experience with graphical interfaces, operating system information, resource monitoring, process management, data visualization, alert logic, and application architecture.

The project will continue to expand as additional modules are developed, tested, and integrated into the main application.
