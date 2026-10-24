# Sentinel — System Monitoring and Management Tool

Sentinel is a Python-based desktop application designed to monitor system performance, view running processes, and organize important system information in one place. It features a professional dark interface with charcoal, black, and grey colors, inspired by modern system management dashboards.

The project is being developed in stages using **Python, PyCharm, and CustomTkinter** on Windows 11.

## Project Overview

Sentinel aims to provide a centralized dashboard for viewing computer performance and managing system information through a clean, user-friendly desktop interface.

The application is organized into five main modules:

1. **Dashboard** — Monitor system performance through live statistics and graphs.
2. **Processes** — View running processes and access process management features.
3. **Hardware Information** — Display information about the computer's hardware and system resources.
4. **Alerts** — Present important system notifications and monitoring alerts.
5. **Reports** — Organize system monitoring information and provide exportable reports.

## Current Development Progress

Sentinel is being developed incrementally, starting with its core foundation before expanding into the remaining modules.

### Completed So Far

- **Project Foundation** — Initial application structure and core components.
- **System Monitoring** — Collect system performance information using Python.
- **Live Performance Graphs** — Display system monitoring data visually.
- **Process Manager Foundation** — Implement the initial process management functionality.
- **Main Application** — Establish the main entry point for launching the desktop application.

### Upcoming Features

- Hardware Information module
- Alerts and notifications module
- Reports and data export module
- Integration and testing of all five modules
- Additional improvements to the interface and application performance

*Development status reflects the current project checkpoint. Features may be expanded or refined as development continues.*

## Technologies Used

- **Python** — Main programming language
- **CustomTkinter** — Modern desktop graphical user interface
- **psutil** — System and process monitoring
- **Matplotlib** — Performance graphs and data visualization
- **PyCharm** — Development environment

## Project Structure

The planned project structure is organized into separate folders to keep the code manageable as new modules are added.

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

**Note:** This represents the planned project structure. Some files and modules are intended for later development stages and may not yet be implemented.

## Installation

### 1. Install Python

Install Python for Windows if it is not already available. Make sure Python is accessible from your terminal.

### 2. Open the Project

Open the Sentinel project folder in PyCharm.

### 3. Install Dependencies

Open the PyCharm terminal and run:

```bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file contains the libraries required by the project.

Expected dependencies include:

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

## Design Goals

Sentinel is designed with the following goals:

- **Clean Interface** — A modern desktop layout with a dark charcoal, black, and grey color palette.
- **Modular Code** — Separate monitoring logic, interface components, and supporting utilities.
- **Real-Time Monitoring** — Present system performance information with continuously updated visualizations where implemented.
- **Maintainability** — Organize the application so that individual modules can be developed and improved independently.
- **Extensibility** — Provide a foundation for adding more system monitoring and management features.

## Development Roadmap

| Stage | Module or Task | Status |
|---|---|---|
| 1 | Project foundation | Completed |
| 2 | System monitoring and live graphs | Completed |
| 3 | Process Manager foundation | Completed |
| 4 | Hardware Information | Planned |
| 5 | Alerts and notifications | Planned |
| 6 | Reports and exports | Planned |
| 7 | Integration, testing, and refinement | Planned |

## Project Purpose

Sentinel is a personal software development project focused on building practical programming skills through a modular Python desktop application. It provides an opportunity to work with graphical interfaces, system monitoring, process management, data visualization, and application architecture.

The project will continue to grow as each module is implemented and integrated into the main application.
