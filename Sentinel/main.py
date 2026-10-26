import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime

from core.system_monitor import SystemMonitor
from core.process_manager import ProcessManager
from core.alert_manager import AlertManager
from ui.hardware import HardwarePage
from ui.alerts import AlertsPage
from ui.reports import ReportsPage


# =========================
# SENTINEL MAIN APPLICATION
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class SentinelApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sentinel | System Monitor")
        self.geometry("1350x850")
        self.minsize(1050, 700)
        self.configure(fg_color="#111111")

        # Core managers
        self.system_monitor = SystemMonitor()
        self.process_manager = ProcessManager()
        self.alert_manager = AlertManager()

        # Navigation and scheduled tasks
        self.current_page = None
        self.after_jobs = []

        # Dashboard graph data
        self.cpu_history = []
        self.ram_history = []
        self.network_history = []
        self.history_limit = 30

        # Process table data
        self.process_search_var = tk.StringVar()

        self.configure_styles()
        self.create_layout()
        self.navigate("Dashboard")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # =========================
    # APPLICATION LAYOUT
    # =========================

    def configure_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background="#202020",
            foreground="#E5E5E5",
            fieldbackground="#202020",
            borderwidth=0,
            rowheight=30,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#303030",
            foreground="#FFFFFF",
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#454545")],
            foreground=[("selected", "#FFFFFF")]
        )

        style.map(
            "Treeview.Heading",
            background=[("active", "#404040")]
        )

    def create_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color="#181818"
        )
        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        self.sidebar.grid_propagate(False)

        # Main content
        self.content_frame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="#111111"
        )
        self.content_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.create_sidebar()

    def create_sidebar(self):
        ctk.CTkLabel(
            self.sidebar,
            text="SENTINEL",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="#FFFFFF"
        ).pack(
            anchor="w",
            padx=24,
            pady=(30, 2)
        )

        ctk.CTkLabel(
            self.sidebar,
            text="SYSTEM MONITOR",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#777777"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 30)
        )

        self.nav_buttons = {}

        navigation_items = [
            ("Dashboard", "Dashboard"),
            ("Processes", "Processes"),
            ("Hardware", "Hardware"),
            ("Alerts", "Alerts"),
            ("Reports", "Reports")
        ]

        for label, page in navigation_items:
            button = ctk.CTkButton(
                self.sidebar,
                text=label,
                height=42,
                corner_radius=8,
                anchor="w",
                font=ctk.CTkFont(size=13),
                fg_color="transparent",
                hover_color="#303030",
                text_color="#BDBDBD",
                command=lambda selected_page=page: self.navigate(
                    selected_page
                )
            )

            button.pack(
                fill="x",
                padx=14,
                pady=4
            )

            self.nav_buttons[page] = button

        # Sidebar footer
        ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color="#333333"
        ).pack(
            fill="x",
            padx=18,
            pady=(25, 12)
        )

        ctk.CTkLabel(
            self.sidebar,
            text="System Utilities",
            font=ctk.CTkFont(size=11),
            text_color="#777777"
        ).pack(
            anchor="w",
            padx=24
        )

        ctk.CTkLabel(
            self.sidebar,
            text="Sentinel v1.0",
            font=ctk.CTkFont(size=11),
            text_color="#666666"
        ).pack(
            anchor="w",
            padx=24,
            pady=(5, 20)
        )

    # =========================
    # NAVIGATION
    # =========================

    def cancel_scheduled_jobs(self):
        for job in self.after_jobs:
            try:
                self.after_cancel(job)
            except (tk.TclError, ValueError):
                pass

        self.after_jobs.clear()

    def schedule_job(self, delay, callback):
        job = self.after(delay, callback)
        self.after_jobs.append(job)
        return job

    def clear_content(self):
        self.cancel_scheduled_jobs()

        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def navigate(self, page):
        self.clear_content()
        self.current_page = page

        for page_name, button in self.nav_buttons.items():
            if page_name == page:
                button.configure(
                    fg_color="#333333",
                    text_color="#FFFFFF"
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color="#BDBDBD"
                )

        if page == "Dashboard":
            self.show_dashboard()

        elif page == "Processes":
            self.show_processes()

        elif page == "Hardware":
            self.show_hardware()

        elif page == "Alerts":
            self.show_alerts()

        elif page == "Reports":
            self.show_reports()

    # =========================
    # SHARED UI HELPERS
    # =========================

    def create_page_header(self, title, description):
        header = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=28,
            pady=(25, 12)
        )

        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=27, weight="bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color="#999999"
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        return header

    def create_metric_card(self, parent, title, initial_value, column):
        card = ctk.CTkFrame(
            parent,
            fg_color="#1D1D1D",
            corner_radius=12
        )
        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=6,
            pady=6
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color="#999999"
        ).pack(
            anchor="w",
            padx=16,
            pady=(15, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text=initial_value,
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="#FFFFFF"
        )
        value_label.pack(
            anchor="w",
            padx=16,
            pady=(0, 15)
        )

        return value_label

    def safe_metric(self, metrics, key, default=0):
        value = metrics.get(key, default)

        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    # =========================
    # DASHBOARD
    # =========================

    def show_dashboard(self):
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        self.create_page_header(
            "Dashboard",
            "Live overview of your computer's performance"
        )

        dashboard_body = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            corner_radius=0
        )
        dashboard_body.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=22,
            pady=(0, 20)
        )
        dashboard_body.grid_columnconfigure(0, weight=1)

        # Metric cards
        cards_frame = ctk.CTkFrame(
            dashboard_body,
            fg_color="transparent"
        )
        cards_frame.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        for column in range(4):
            cards_frame.grid_columnconfigure(column, weight=1)

        self.cpu_value = self.create_metric_card(
            cards_frame, "CPU USAGE", "0%", 0
        )
        self.ram_value = self.create_metric_card(
            cards_frame, "MEMORY USAGE", "0%", 1
        )
        self.disk_value = self.create_metric_card(
            cards_frame, "DISK USAGE", "0%", 2
        )
        self.network_value = self.create_metric_card(
            cards_frame, "DOWNLOAD SPEED", "0 KB/s", 3
        )

        # System information panel
        self.info_panel = ctk.CTkFrame(
            dashboard_body,
            fg_color="#1D1D1D",
            corner_radius=12
        )
        self.info_panel.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=6,
            pady=(12, 6)
        )

        self.info_label = ctk.CTkLabel(
            self.info_panel,
            text="Loading system information...",
            font=ctk.CTkFont(size=12),
            text_color="#BBBBBB",
            justify="left",
            anchor="w"
        )
        self.info_label.pack(
            fill="x",
            padx=18,
            pady=15
        )

        # Graphs panel
        graph_panel = ctk.CTkFrame(
            dashboard_body,
            fg_color="#1D1D1D",
            corner_radius=12
        )
        graph_panel.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=6,
            pady=6
        )
        graph_panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            graph_panel,
            text="Performance History",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        ).pack(
            anchor="w",
            padx=16,
            pady=(14, 0)
        )

        self.figure = Figure(
            figsize=(9, 4.3),
            dpi=100,
            facecolor="#1D1D1D"
        )

        self.cpu_axis = self.figure.add_subplot(211)
        self.network_axis = self.figure.add_subplot(212)

        self.figure.subplots_adjust(
            left=0.09,
            right=0.97,
            top=0.94,
            bottom=0.10,
            hspace=0.55
        )

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=graph_panel
        )
        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.update_dashboard()

    def update_dashboard(self):
        if self.current_page != "Dashboard":
            return

        try:
            metrics = self.system_monitor.get_metrics()

            cpu = self.safe_metric(metrics, "cpu")
            ram = self.safe_metric(metrics, "ram")
            disk = self.safe_metric(metrics, "disk")

            download_speed = self.safe_metric(
                metrics, "download_speed"
            )
            upload_speed = self.safe_metric(
                metrics, "upload_speed"
            )

            self.cpu_value.configure(
                text=f"{cpu:.1f}%"
            )
            self.ram_value.configure(
                text=f"{ram:.1f}%"
            )
            self.disk_value.configure(
                text=f"{disk:.1f}%"
            )
            self.network_value.configure(
                text=self.system_monitor.format_speed(download_speed)
            )

            computer = metrics.get("computer", "Unknown")
            operating_system = metrics.get("os", "Unknown")
            processor = metrics.get("processor", "Unknown")
            uptime = metrics.get("uptime", "Unknown")

            self.info_label.configure(
                text=(
                    f"Computer: {computer}     "
                    f"Operating System: {operating_system}\n"
                    f"Processor: {processor}\n"
                    f"Uptime: {uptime}\n"
                    f"Upload: {self.system_monitor.format_speed(upload_speed)}"
                    f"     Download: "
                    f"{self.system_monitor.format_speed(download_speed)}"
                )
            )

            self.cpu_history.append(cpu)
            self.ram_history.append(ram)
            self.network_history.append(
                download_speed / 1024
            )

            self.cpu_history = self.cpu_history[-self.history_limit:]
            self.ram_history = self.ram_history[-self.history_limit:]
            self.network_history = self.network_history[-self.history_limit:]

            self.update_dashboard_graphs()

            # Check for system resource alerts
            self.alert_manager.check_metrics(metrics)

        except Exception as error:
            self.info_label.configure(
                text=f"Unable to refresh dashboard: {error}"
            )

        self.schedule_job(2000, self.update_dashboard)

    def update_dashboard_graphs(self):
        points = list(range(1, len(self.cpu_history) + 1))

        self.cpu_axis.clear()
        self.cpu_axis.set_facecolor("#1D1D1D")
        self.cpu_axis.plot(
            points,
            self.cpu_history,
            label="CPU",
            linewidth=2
        )
        self.cpu_axis.plot(
            points,
            self.ram_history,
            label="RAM",
            linewidth=2
        )
        self.cpu_axis.set_title(
            "CPU and RAM Usage (%)",
            color="#FFFFFF",
            fontsize=10
        )
        self.cpu_axis.set_ylim(0, 100)
        self.cpu_axis.tick_params(
            colors="#AAAAAA",
            labelsize=8
        )
        self.cpu_axis.grid(
            True,
            alpha=0.15
        )
        self.cpu_axis.legend(
            facecolor="#292929",
            labelcolor="#FFFFFF",
            fontsize=8
        )

        self.network_axis.clear()
        self.network_axis.set_facecolor("#1D1D1D")
        self.network_axis.plot(
            points,
            self.network_history,
            label="Download",
            linewidth=2
        )
        self.network_axis.set_title(
            "Network Download (KB/s)",
            color="#FFFFFF",
            fontsize=10
        )
        self.network_axis.tick_params(
            colors="#AAAAAA",
            labelsize=8
        )
        self.network_axis.grid(
            True,
            alpha=0.15
        )
        self.network_axis.legend(
            facecolor="#292929",
            labelcolor="#FFFFFF",
            fontsize=8
        )

        self.canvas.draw_idle()

    # =========================
    # PROCESS MANAGER
    # =========================

    def show_processes(self):
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        self.create_page_header(
            "Process Manager",
            "View, search, and manage running processes"
        )

        toolbar = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        toolbar.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=28,
            pady=(0, 12)
        )

        toolbar.grid_columnconfigure(0, weight=1)

        self.process_search_var = tk.StringVar()

        search_entry = ctk.CTkEntry(
            toolbar,
            textvariable=self.process_search_var,
            placeholder_text="Search by process name or PID...",
            height=36
        )
        search_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        search_entry.bind(
            "<KeyRelease>",
            lambda event: self.refresh_processes()
        )

        ctk.CTkButton(
            toolbar,
            text="Refresh",
            width=100,
            height=36,
            fg_color="#353535",
            hover_color="#4A4A4A",
            command=self.refresh_processes
        ).grid(
            row=0,
            column=1,
            padx=(0, 8)
        )

        ctk.CTkButton(
            toolbar,
            text="End Process",
            width=120,
            height=36,
            fg_color="#6B3030",
            hover_color="#853838",
            command=self.end_selected_process
        ).grid(
            row=0,
            column=2
        )

        table_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="#1D1D1D",
            corner_radius=10
        )
        table_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=28,
            pady=(0, 10)
        )
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        columns = (
            "pid",
            "name",
            "username",
            "cpu",
            "memory",
            "status"
        )

        self.process_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "pid": "PID",
            "name": "Process Name",
            "username": "User",
            "cpu": "CPU %",
            "memory": "Memory (MB)",
            "status": "Status"
        }

        widths = {
            "pid": 80,
            "name": 250,
            "username": 180,
            "cpu": 100,
            "memory": 130,
            "status": 130
        }

        for column in columns:
            self.process_tree.heading(
                column,
                text=headings[column]
            )
            self.process_tree.column(
                column,
                width=widths[column],
                minwidth=60,
                anchor="w"
            )

        vertical_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.process_tree.yview
        )
        horizontal_scroll = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.process_tree.xview
        )

        self.process_tree.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )

        self.process_tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        vertical_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )
        horizontal_scroll.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        self.process_status_label = ctk.CTkLabel(
            self.content_frame,
            text="Loading processes...",
            text_color="#999999",
            font=ctk.CTkFont(size=11)
        )
        self.process_status_label.grid(
            row=3,
            column=0,
            sticky="w",
            padx=30,
            pady=(0, 15)
        )

        self.refresh_processes()
        self.schedule_job(5000, self.auto_refresh_processes)

    def auto_refresh_processes(self):
        if self.current_page != "Processes":
            return

        self.refresh_processes()
        self.schedule_job(5000, self.auto_refresh_processes)

    def refresh_processes(self):
        if not hasattr(self, "process_tree"):
            return

        try:
            processes = self.process_manager.get_processes()
            search_text = self.process_search_var.get().strip().lower()

            for item in self.process_tree.get_children():
                self.process_tree.delete(item)

            displayed_count = 0

            for process in processes:
                pid = process.get("pid", "")
                name = process.get("name", "Unknown")
                username = process.get("username", "")
                cpu = process.get("cpu_percent", process.get("cpu", 0))
                memory = process.get(
                    "memory_mb",
                    process.get("memory", 0)
                )
                status = process.get("status", "Unknown")

                searchable_text = f"{pid} {name}".lower()

                if search_text and search_text not in searchable_text:
                    continue

                try:
                    cpu_text = f"{float(cpu):.1f}%"
                except (TypeError, ValueError):
                    cpu_text = str(cpu)

                try:
                    memory_text = f"{float(memory):.1f}"
                except (TypeError, ValueError):
                    memory_text = str(memory)

                self.process_tree.insert(
                    "",
                    "end",
                    values=(
                        pid,
                        name,
                        username,
                        cpu_text,
                        memory_text,
                        status
                    )
                )

                displayed_count += 1

            self.process_status_label.configure(
                text=(
                    f"Showing {displayed_count} processes. "
                    f"Refreshes automatically every 5 seconds."
                )
            )

        except Exception as error:
            self.process_status_label.configure(
                text=f"Unable to load processes: {error}",
                text_color="#FF7777"
            )

    def end_selected_process(self):
        selected = self.process_tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Process Selected",
                "Please select a process first.",
                parent=self
            )
            return

        values = self.process_tree.item(
            selected[0],
            "values"
        )

        pid = values[0]
        process_name = values[1]

        confirmed = messagebox.askyesno(
            "Confirm Process Termination",
            (
                f"Are you sure you want to end this process?\n\n"
                f"Process: {process_name}\n"
                f"PID: {pid}\n\n"
                "Ending system processes may affect Windows or "
                "running applications."
            ),
            parent=self
        )

        if not confirmed:
            return

        try:
            result = self.process_manager.terminate_process(int(pid))

            if result is False:
                messagebox.showerror(
                    "Termination Failed",
                    f"Could not terminate {process_name}.",
                    parent=self
                )
            else:
                messagebox.showinfo(
                    "Process Manager",
                    f"Termination request sent for {process_name} (PID {pid}).",
                    parent=self
                )

            self.refresh_processes()

        except Exception as error:
            messagebox.showerror(
                "Termination Error",
                f"Could not terminate the selected process.\n\n{error}",
                parent=self
            )

    # =========================
    # HARDWARE INFORMATION
    # =========================

    def show_hardware(self):
        page = HardwarePage(self.content_frame)
        page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    # =========================
    # ALERTS
    # =========================

    def show_alerts(self):
        page = AlertsPage(
            self.content_frame,
            alert_manager=self.alert_manager
        )
        page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        page.set_metric_provider(
            self.system_monitor.get_metrics
        )
        page.refresh_alerts()

    # =========================
    # REPORTS
    # =========================

    def show_reports(self):
        page = ReportsPage(
            self.content_frame,
            system_monitor=self.system_monitor,
            process_manager=self.process_manager,
            alert_manager=self.alert_manager
        )

        page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    # =========================
    # CLOSE APPLICATION
    # =========================

    def on_close(self):
        self.cancel_scheduled_jobs()
        self.destroy()


# =========================
# RUN SENTINEL
# =========================

if __name__ == "__main__":
    app = SentinelApp()
    app.mainloop()
