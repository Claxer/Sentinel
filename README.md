# Sentinel — System Monitoring and Management Tool

Sentinel is a Python-based desktop application designed to monitor system performance, view and manage running processes, display hardware information, detect potential system resource issues, and export useful system reports. It features a professional dark interface using charcoal, black, and grey colors, inspired by modern system management dashboards.

The project is being developed using **Python, PyCharm, CustomTkinter, psutil, and Matplotlib** on Windows 11.

## Project Overview

Sentinel provides a centralized dashboard for monitoring computer performance, viewing hardware specifications, managing running processes, identifying potential system resource issues, and exporting monitoring data into CSV reports.

The application includes six main modules:

1. **Dashboard** — Monitor CPU, memory, disk, and network activity through live statistics and performance graphs.
2. **Processes** — View running processes, search by process name or PID, inspect resource usage, and request process termination.
3. **Hardware Information** — Display processor specifications, memory information, storage drives, network adapters, battery status, temperature readings where supported, and operating system details.
4. **Alerts** — Detect high CPU usage, high memory usage, and high disk usage based on configured thresholds.
5. **Reports** — Generate and export system metrics, running process information, active alerts, and alert history as CSV files.
6. **Settings** — Configure alert thresholds and automatic dashboard and process refresh intervals, with settings saved locally in a JSON file.

## Current Development Progress

Sentinel is developed in stages, starting with core monitoring components and integrating additional functionality into the desktop interface.

### Implemented Features

- **Project Foundation** — Established the main application entry point and modular project structure.
- **System Monitoring** — Collect CPU usage, RAM usage, disk usage, network transfer speeds, computer information, and system uptime using `psutil`.
- **Live Performance Graphs** — Display CPU and RAM usage alongside network download activity using Matplotlib.
- **Automatic Dashboard Updates** — Refresh system metrics and graphs periodically.
- **Process Manager** — Collect and display running processes with their PID, name, CPU usage, memory usage, username, and status.
- **Safer Process Enumeration** — Skip processes that disappear or cannot be accessed while process information is being collected.
- **Process Sorting** — Sort collected processes by CPU usage.
- **Process Search** — Search for processes by name or process ID.
- **Process Details** — Retrieve information about a selected process, including available process information, and return a clear success or error result.
- **Process Termination** — Validate process IDs, prevent attempts to terminate Sentinel itself, request termination, and wait up to three seconds for the process to exit.
- **Process Termination Safety** — Avoid automatically force-killing a process if it does not exit within the timeout.
- **Process Error Handling** — Handle inaccessible, invalid, or already-terminated processes without unnecessarily interrupting process collection.
- **Automatic Process Refresh** — Refresh the process list periodically.
- **Hardware Information** — Collect processor details, physical and logical cores, CPU frequency where available, RAM and swap usage, storage capacity, network adapter details, and system information.
- **Battery Information** — Retrieve battery percentage, power connection status, and estimated remaining time when supported.
- **Temperature Information** — Attempt to retrieve hardware temperature readings when the operating system and hardware expose them through `psutil`.
- **Network Adapter Details** — Display adapter status, available IPv4 addresses, reported link speed, and cumulative sent and received data.
- **Alert Manager** — Monitor CPU, RAM, and disk usage against configurable thresholds.
- **Alert Severity** — Classify resource alerts as Warning or Critical according to configured limits and current readings.
- **Active Alert Summary** — Display summary counts for active alerts and Critical alerts on the Alerts page.
- **Active Alert Cards** — Display alert titles, severity, descriptions, timestamps, and available current values and configured thresholds.
- **Alert Refresh** — Refresh active alerts and alert history through the Alerts page.
- **Metric Integration** — Allow the Alerts page to request current metrics from a configured provider and check them through the alert manager.
- **Alert History Display** — Retrieve and display recorded alert events, including events that are no longer active.
- **Newest-First History Display** — Show the most recently recorded alert events first.
- **Persistent Alert History** — Load previously saved alert events from `data/alert_history.json` and save new events.
- **Duplicate Alert Prevention** — Record an alert when it first becomes active instead of repeatedly recording it on every monitoring refresh.
- **Alert History Management** — Clear saved alert-history events through the Alerts page, with a confirmation prompt before deletion.
- **Alert Empty States** — Display helpful messages when no active alerts or history events are available.
- **Settings Manager** — Load, validate, update, and save application settings in `settings.json`.
- **Configurable Alert Thresholds** — Set CPU, RAM, and disk alert thresholds through the Settings page.
- **Configurable Refresh Intervals** — Set the dashboard refresh interval and process list refresh interval.
- **Settings Validation** — Restrict resource thresholds to 1–100%, dashboard refresh to 1–60 seconds, and process refresh to 2–300 seconds.
- **Settings Reset** — Restore the default settings when needed.
- **Settings Integration** — Apply saved alert thresholds to the shared alert manager and use configured intervals for scheduled dashboard and process refreshes.
- **System Metrics Report** — Export current system metrics, including available CPU, memory, disk, network, and other monitoring information.
- **Process Report** — Export information about currently running processes.
- **Active Alerts Report** — Export alerts that are currently active.
- **Alert History Report** — Export recorded alert events.
- **CSV Export** — Save reports as `.csv` files that can be opened in spreadsheet applications.
- **Save Location Selection** — Choose the destination and filename for exported reports through a save-file dialog.
- **Export Feedback** — Display success or error messages when exporting reports.
- **Dark Interface** — Use a consistent dark-themed desktop layout with charcoal, black, and grey colors.

### Current Limitations

- Alert history is persisted locally in `data/alert_history.json` and is limited to the 200 most recent events.
- Settings are stored locally in `settings.json` and are not synchronized between devices.
- Reports contain a snapshot of the information available when the export is requested; continuous historical metric recording is not yet implemented.
- Hardware temperature readings depend on available sensor support and may not appear on some Windows computers.
- Battery information is unavailable on systems without a supported battery interface.
- CPU frequency and network link speed may not be reported on every system.
- Process information may be unavailable for protected or short-lived processes.
- Process termination may fail when administrator permissions are required or the operating system prevents access.
- Ending essential system processes may cause instability.
- The application requests process termination but does not automatically force-kill a process if it does not exit within three seconds.
- The Alerts page depends on a working connection to the alert manager. Its metric-refresh feature requires a metric provider to be configured by the main application.
- Storage usage information does not currently provide a complete SSD or HDD health assessment.
- The application is still under development, and further testing and performance improvements are planned.

## Technologies Used

- **Python** — Main programming language.
- **CustomTkinter** — Modern desktop graphical user interface.
- **psutil** — System resource, process, network, disk, and battery information.
- **Matplotlib** — Live performance graphs and data visualization.
- **Tkinter and ttk** — Native interface components, process tables, scrollbars, file dialogs, and confirmation messages.
- **CSV module** — Export monitoring information into comma-separated value files.
- **JSON** — Store application settings and alert history.
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
│   ├── settings_manager.py
│   └── report_manager.py
│
├── ui/
│   ├── __init__.py
│   ├── hardware.py
│   ├── alerts.py
│   ├── reports.py
│   └── settings.py
│
├── data/
│   └── alert_history.json
│
├── settings.json
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

**Note:** This is an overview of the project structure, including folders reserved for future development. Some listed database and utility files may not exist yet. The `data/alert_history.json` file may also be created automatically when alert history is saved.

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

The CSV and JSON functionality uses Python's built-in modules, so additional packages are not required for those features.

### 4. Run Sentinel

From the project's root directory, run:

```bash
python main.py
```

The main window should open with navigation for Dashboard, Processes, Hardware, Alerts, Reports, and Settings.

On first launch, `settings.json` is created automatically with default settings. The `data/alert_history.json` file and its parent folder are created when alert history is saved; the history file may not exist until an alert is recorded or history is explicitly saved.

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

The Process Manager provides a searchable view of running processes and supports controlled process termination. Its core logic is located in `core/process_manager.py`.

#### Process Information

- Process ID (PID) and process name.
- CPU usage and memory consumption.
- Username and process status.
- Memory usage reported in megabytes.
- Processes sorted by CPU usage.
- Search by process name or PID through the application interface.
- Periodic process list refresh through the application interface.

The process manager returns process information as dictionaries containing fields such as `pid`, `name`, `username`, `memory`, `memory_mb`, `cpu`, `cpu_percent`, and `status`. Some fields may contain fallback values if information is unavailable.

#### Process Details

The `get_process_details(pid)` method retrieves available information about a selected process, such as:

- Process ID and name.
- Username and status.
- CPU usage and memory usage.
- Creation time, executable path, and command line when accessible.

The method returns a structured result containing `success`, `message`, and `process` fields. If a process cannot be found or accessed, it returns an error result rather than assuming the requested information is available.

#### Process Safety and Error Handling

- Skip processes that disappear during collection.
- Handle access-denied and other process-related errors.
- Ignore inaccessible or short-lived processes during process enumeration.
- Validate process IDs before requesting termination.
- Prevent attempts to terminate Sentinel's own process.
- Request process termination and wait up to three seconds for the process to exit.
- Return a success or error message when retrieving details or terminating a process.
- Do not automatically force-kill a process if it does not exit within the timeout.

Process termination is subject to operating system permissions. Some protected processes cannot be terminated without administrator privileges. Use this feature carefully because ending essential system processes may cause instability.

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

Some hardware values depend on what the operating system and hardware expose to Python.

### Alerts

The Alerts page uses `ui/alerts.py` to present active alerts and alert history, while `core/alert_manager.py` handles resource threshold checks and persistent history.

#### Default Alert Thresholds

| Resource | Default threshold |
|---|---:|
| CPU usage | 85% |
| RAM usage | 85% |
| Disk usage | 90% |

Readings at or above 95% are classified as Critical by the alert manager.

#### Alerts Page Interface

The updated Alerts page uses a dark interface with summary cards and separate scrollable sections for active alerts and alert history.

- **Active Alerts Summary** — Shows the number of currently active alerts.
- **Critical Summary** — Shows how many active alerts are classified as Critical.
- **History Summary** — Shows the number of recorded history events.
- **Active Alert Cards** — Display alert titles, severity, descriptions, and available timestamps.
- **Alert Measurements** — Show current values and configured thresholds when those fields are provided by the alert manager.
- **Refresh Alerts** — Refresh active alerts and history.
- **Metric Integration** — Request current system metrics through a configured metric provider and pass them to the alert manager for checking.
- **Alert History Display** — View recorded events, including alerts that may no longer be active.
- **Newest-First History** — Display the newest saved events at the top.
- **Clear History** — Ask for confirmation before clearing saved history events.
- **Empty-State Messages** — Display helpful messages when there are no alerts, no history events, or no alert manager available.
- **Refresh Error Handling** — Display a status message if refreshing alert information fails.

#### Alert Manager Features

- Monitor CPU, RAM, and disk usage against configured thresholds.
- Classify alerts as Warning or Critical.
- Retrieve currently active alerts through `get_active_alerts()`.
- Retrieve recorded events through `get_alert_history()`.
- Save and load history through `data/alert_history.json`.
- Avoid repeatedly recording the same alert while it remains continuously active.
- Clear recorded history through `clear_history()`.
- Apply configurable thresholds managed by the Settings page.

The Alerts page expects the alert manager to provide the methods `check_metrics(metrics)`, `get_active_alerts()`, `get_alert_history()`, and `clear_history()`. Its metric-refresh feature also requires the main application to configure a metric provider using `set_metric_provider(provider)`.

Clearing history removes saved history events; it does not change the configured resource thresholds or necessarily resolve currently active alerts.

### Settings

The Settings page uses `core/settings_manager.py` to manage Sentinel's local configuration. The shared settings manager loads existing settings at startup, validates changes, and saves valid settings to `settings.json` in the project root.

#### Available Settings

| Setting | Default | Allowed range |
|---|---:|---:|
| CPU alert threshold | 85% | 1–100% |
| RAM alert threshold | 85% | 1–100% |
| Disk alert threshold | 90% | 1–100% |
| Dashboard refresh interval | 2 seconds | 1–60 seconds |
| Process list refresh interval | 5 seconds | 2–300 seconds |

#### Settings Features

- Load settings from `settings.json`.
- Create default settings automatically when the file does not exist.
- Validate values before saving.
- Save changes through the Settings page.
- Reset settings to their default values.
- Apply alert thresholds to the shared `AlertManager`.
- Use configured intervals for scheduled dashboard and process-list updates.

Changes to refresh intervals affect subsequent scheduled refreshes. Settings are stored locally on the computer and are not synchronized to another device.

### Reports

The Reports module allows users to export useful monitoring information without manually copying data from the application.

#### Available Reports

**1. System Metrics Report**

Exports the system metrics currently returned by `SystemMonitor`, such as CPU usage, RAM usage, disk usage, network speeds, computer information, and uptime when those values are available.

**2. Process Report**

Exports the current process list returned by `ProcessManager`. Depending on the process information provided by the system, the report can include process IDs, names, usernames, memory usage, CPU usage, and process status.

**3. Active Alerts Report**

Exports alerts that are active at the time of the request, including available timestamps, titles, descriptions, severity, measured values, configured limits, and status.

**4. Alert History Report**

Exports recorded alert events, including previously triggered alerts that may no longer be active.

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
- Alert history is stored in `data/alert_history.json` and can persist between application sessions.
- If no alerts or processes are available, the report may contain an appropriate empty-state message.
- Database-backed report storage and long-term historical analysis remain potential future improvements.

### Report File Examples

Sentinel may generate filenames similar to these:

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
- **Process Safety** — Handle unavailable processes and prevent unsafe termination attempts where possible.
- **System Diagnostics** — Collect hardware, storage, network, and operating system information.
- **Alert Monitoring** — Identify resource usage that exceeds configured thresholds.
- **Alert History** — Preserve and display recorded alert events between application sessions.
- **Report Generation** — Make monitoring information available as exportable CSV files.
- **Maintainability** — Develop individual modules independently while preserving existing functionality.
- **Extensibility** — Provide a foundation for persistent monitoring history, report generation, and additional diagnostics.

## Development Roadmap

| Stage | Module or Task | Status |
|---|---|---|
| 1 | Project foundation and main application | Implemented |
| 2 | System monitoring and live graphs | Implemented |
| 3 | Process Manager | Implemented; safer process handling added |
| 4 | Hardware Information module | Implemented; further refinement planned |
| 5 | Alert Manager and Alerts page | Implemented; summary cards, refresh, and history controls added |
| 6 | Reports page and CSV exports | Implemented; testing and refinement planned |
| 7 | Settings page and JSON configuration manager | Implemented; testing and refinement planned |
| 8 | Persistent alert history in JSON with Alerts page history display and controls | Implemented |
| 9 | Database-backed monitoring history | Planned |
| 10 | Integration testing, performance optimization, and refinement | In progress |

## Project Purpose

Sentinel is a personal software development project focused on building practical programming and IT skills through a modular Python desktop application.

It provides hands-on experience with graphical user interfaces, operating system information, resource monitoring, process management, data visualization, alert logic, CSV file handling, and application architecture.

The project will continue to expand as additional modules are developed, tested, and integrated into the application.
