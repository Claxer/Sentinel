import customtkinter as ctk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from core.system_monitor import SystemMonitor
from core.process_manager import ProcessManager


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class SentinelApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Sentinel | System Monitor")
        self.geometry("1250x820")
        self.minsize(1000, 680)
        self.configure(fg_color="#111315")

        self.bg_color = "#111315"
        self.sidebar_color = "#191c20"
        self.card_color = "#202429"
        self.text_color = "#f1f3f5"
        self.muted_color = "#9299a3"

        self.current_page = "Dashboard"
        self.monitor = SystemMonitor()
        self.process_manager = ProcessManager()

        self.refresh_job = None
        self.process_refresh_job = None
        self.process_data = []

        self.history_limit = 30
        self.cpu_history = []
        self.ram_history = []
        self.download_history = []
        self.upload_history = []

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()
        self.navigate("Dashboard")

        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, width=220, corner_radius=0,
            fg_color=self.sidebar_color
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.sidebar,
            text="SENTINEL",
            font=ctk.CTkFont(size=23, weight="bold"),
            text_color=self.text_color
        ).grid(row=0, column=0, padx=24, pady=(30, 4), sticky="w")

        ctk.CTkLabel(
            self.sidebar,
            text="SMART SYSTEM MONITOR",
            font=ctk.CTkFont(size=10),
            text_color=self.muted_color
        ).grid(row=1, column=0, padx=25, pady=(0, 32), sticky="w")

        self.nav_buttons = {}

        for index, page in enumerate(
            ["Dashboard", "Processes", "Hardware", "Alerts", "Reports"],
            start=2
        ):
            button = ctk.CTkButton(
                self.sidebar,
                text=page,
                height=42,
                anchor="w",
                corner_radius=8,
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                hover_color="#2a2e35",
                text_color=self.text_color,
                command=lambda name=page: self.navigate(name)
            )
            button.grid(
                row=index, column=0, padx=14, pady=4, sticky="ew"
            )
            self.nav_buttons[page] = button

        self.sidebar.grid_rowconfigure(8, weight=1)

        footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer.grid(row=9, column=0, padx=20, pady=20, sticky="ew")

        ctk.CTkLabel(
            footer, text="SENTINEL",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.muted_color
        ).pack(anchor="w")

        ctk.CTkLabel(
            footer, text="Version 1.0.0",
            font=ctk.CTkFont(size=11),
            text_color=self.muted_color
        ).pack(anchor="w", pady=(3, 0))

    def create_main_area(self):
        self.main_area = ctk.CTkFrame(
            self, corner_radius=0, fg_color=self.bg_color
        )
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(0, weight=1)

        self.content = ctk.CTkFrame(
            self.main_area, fg_color="transparent"
        )
        self.content.grid(
            row=0, column=0, sticky="nsew", padx=25, pady=22
        )

    def clear_content(self):
        if self.refresh_job is not None:
            self.after_cancel(self.refresh_job)
            self.refresh_job = None

        if self.process_refresh_job is not None:
            self.after_cancel(self.process_refresh_job)
            self.process_refresh_job = None

        for widget in self.content.winfo_children():
            widget.destroy()

    def navigate(self, page):
        self.current_page = page

        for name, button in self.nav_buttons.items():
            button.configure(
                fg_color="#303746" if name == page else "transparent",
                text_color="#ffffff" if name == page else self.text_color
            )

        if page == "Dashboard":
            self.show_dashboard()
        elif page == "Processes":
            self.show_processes()
        else:
            self.show_placeholder(page)

    def create_metric_card(self, title, value, row, column):
        card = ctk.CTkFrame(
            self.content, fg_color=self.card_color, corner_radius=12
        )
        card.grid(
            row=row, column=column, padx=6, pady=6, sticky="ew"
        )

        ctk.CTkLabel(
            card, text=title,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.muted_color
        ).pack(anchor="w", padx=16, pady=(12, 3))

        value_label = ctk.CTkLabel(
            card, text=value,
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color=self.text_color
        )
        value_label.pack(anchor="w", padx=16, pady=(0, 12))
        return value_label

    def show_dashboard(self):
        self.clear_content()
        self.content.grid_columnconfigure((0, 1), weight=1)

        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.grid(
            row=0, column=0, columnspan=2,
            sticky="ew", pady=(0, 15)
        )

        ctk.CTkLabel(
            header, text="System Overview",
            font=ctk.CTkFont(size=27, weight="bold"),
            text_color=self.text_color
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Live performance monitoring and system statistics",
            font=ctk.CTkFont(size=13),
            text_color=self.muted_color
        ).pack(anchor="w", pady=(4, 0))

        self.cpu_value = self.create_metric_card(
            "CPU USAGE", "0%", 1, 0
        )
        self.ram_value = self.create_metric_card(
            "MEMORY USAGE", "0%", 1, 1
        )
        self.disk_value = self.create_metric_card(
            "DISK USAGE", "0%", 2, 0
        )
        self.network_value = self.create_metric_card(
            "NETWORK ACTIVITY", "0 KB/s", 2, 1
        )

        chart_frame = ctk.CTkFrame(
            self.content, fg_color=self.card_color, corner_radius=12
        )
        chart_frame.grid(
            row=3, column=0, columnspan=2,
            sticky="nsew", pady=(15, 0)
        )
        self.content.grid_rowconfigure(3, weight=1)

        self.figure = Figure(
            figsize=(8, 3.4), dpi=100, facecolor=self.card_color
        )
        self.cpu_axis = self.figure.add_subplot(211)
        self.network_axis = self.figure.add_subplot(212)

        self.configure_axis(self.cpu_axis, "CPU AND MEMORY USAGE", "%")
        self.configure_axis(
            self.network_axis, "NETWORK DOWNLOAD AND UPLOAD", "KB/s"
        )
        self.figure.tight_layout(pad=2.2)

        self.chart_canvas = FigureCanvasTkAgg(
            self.figure, master=chart_frame
        )
        self.chart_canvas.get_tk_widget().pack(
            fill="both", expand=True, padx=10, pady=10
        )

        self.system_label = ctk.CTkLabel(
            self.content, text="Loading system information...",
            font=ctk.CTkFont(size=11),
            text_color=self.muted_color, justify="left"
        )
        self.system_label.grid(
            row=4, column=0, columnspan=2,
            sticky="ew", pady=(12, 0)
        )

        self.update_metrics()

    def configure_axis(self, axis, title, ylabel):
        axis.set_facecolor(self.card_color)
        axis.set_title(
            title, color=self.text_color, fontsize=9, loc="left"
        )
        axis.set_ylabel(ylabel, color=self.muted_color, fontsize=8)
        axis.tick_params(colors=self.muted_color, labelsize=8)
        axis.grid(color="#393e45", alpha=0.6)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.spines["bottom"].set_color("#393e45")
        axis.spines["left"].set_color("#393e45")

    def update_metrics(self):
        if self.current_page != "Dashboard":
            return

        try:
            data = self.monitor.get_metrics()

            self.cpu_value.configure(text=f"{data['cpu']:.1f}%")
            self.ram_value.configure(text=f"{data['ram']:.1f}%")
            self.disk_value.configure(text=f"{data['disk']:.1f}%")

            self.network_value.configure(
                text=(
                    f"{self.monitor.format_speed(data['download_speed'])} / "
                    f"{self.monitor.format_speed(data['upload_speed'])}"
                )
            )

            self.cpu_history.append(data["cpu"])
            self.ram_history.append(data["ram"])
            self.download_history.append(data["download_speed"] / 1024)
            self.upload_history.append(data["upload_speed"] / 1024)

            self.cpu_history = self.cpu_history[-self.history_limit:]
            self.ram_history = self.ram_history[-self.history_limit:]
            self.download_history = self.download_history[-self.history_limit:]
            self.upload_history = self.upload_history[-self.history_limit:]

            x_values = list(range(len(self.cpu_history)))

            self.cpu_axis.clear()
            self.configure_axis(
                self.cpu_axis, "CPU AND MEMORY USAGE", "%"
            )
            self.cpu_axis.set_ylim(0, 100)
            self.cpu_axis.plot(
                x_values, self.cpu_history,
                color="#8b9cf6", label="CPU"
            )
            self.cpu_axis.plot(
                x_values, self.ram_history,
                color="#65c8a0", label="RAM"
            )
            self.cpu_axis.legend(
                facecolor=self.card_color,
                labelcolor=self.text_color, fontsize=8
            )

            self.network_axis.clear()
            self.configure_axis(
                self.network_axis, "NETWORK DOWNLOAD AND UPLOAD", "KB/s"
            )
            self.network_axis.plot(
                x_values, self.download_history,
                color="#8b9cf6", label="Download"
            )
            self.network_axis.plot(
                x_values, self.upload_history,
                color="#e6b566", label="Upload"
            )
            self.network_axis.legend(
                facecolor=self.card_color,
                labelcolor=self.text_color, fontsize=8
            )

            self.figure.tight_layout(pad=2.2)
            self.chart_canvas.draw_idle()

            self.system_label.configure(
                text=(
                    f"Computer: {data['computer']}  |  OS: {data['os']}  |  "
                    f"Physical cores: {data['physical_cores']}  |  "
                    f"Logical cores: {data['logical_cores']}\n"
                    f"RAM: {data['ram_used_gb']:.2f} / "
                    f"{data['ram_total_gb']:.2f} GB  |  "
                    f"Disk: {data['disk_used_gb']:.1f} / "
                    f"{data['disk_total_gb']:.1f} GB  |  "
                    f"Uptime: {data['uptime']}"
                )
            )

        except (OSError, RuntimeError, ValueError, KeyError) as error:
            self.system_label.configure(text=f"Monitoring error: {error}")

        self.refresh_job = self.after(1000, self.update_metrics)

    def show_processes(self):
        self.clear_content()
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self.content, text="Process Manager",
            font=ctk.CTkFont(size=27, weight="bold"),
            text_color=self.text_color
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            self.content,
            text="Inspect running applications and their resource usage.",
            font=ctk.CTkFont(size=13),
            text_color=self.muted_color
        ).grid(row=1, column=0, sticky="w", pady=(5, 18))

        toolbar = ctk.CTkFrame(
            self.content, fg_color="transparent"
        )
        toolbar.grid(row=2, column=0, sticky="new", pady=(0, 12))
        toolbar.grid_columnconfigure(0, weight=1)

        self.process_search = ctk.CTkEntry(
            toolbar,
            placeholder_text="Search process name or PID...",
            height=38
        )
        self.process_search.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.process_search.bind(
            "<KeyRelease>", lambda event: self.populate_process_table()
        )

        ctk.CTkButton(
            toolbar, text="Refresh", width=100, height=38,
            command=self.refresh_processes
        ).grid(row=0, column=1, padx=4)

        ctk.CTkButton(
            toolbar, text="End Process", width=120, height=38,
            fg_color="#843e45", hover_color="#a64c55",
            command=self.end_selected_process
        ).grid(row=0, column=2, padx=(4, 0))

        table_frame = ctk.CTkFrame(
            self.content, fg_color=self.card_color, corner_radius=10
        )
        table_frame.grid(row=3, column=0, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(3, weight=1)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Sentinel.Treeview",
            background="#202429",
            foreground="#f1f3f5",
            fieldbackground="#202429",
            rowheight=30,
            borderwidth=0
        )
        style.configure(
            "Sentinel.Treeview.Heading",
            background="#303640",
            foreground="#ffffff",
            relief="flat"
        )
        style.map(
            "Sentinel.Treeview",
            background=[("selected", "#46516b")],
            foreground=[("selected", "#ffffff")]
        )

        columns = ("pid", "name", "cpu", "memory", "status")

        self.process_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Sentinel.Treeview",
            selectmode="browse"
        )

        headings = {
            "pid": ("PID", 80),
            "name": ("Process Name", 250),
            "cpu": ("CPU %", 100),
            "memory": ("Memory (MB)", 120),
            "status": ("Status", 130)
        }

        for column, (heading, width) in headings.items():
            self.process_table.heading(
                column,
                text=heading,
                command=lambda c=column: self.sort_processes(c)
            )
            self.process_table.column(
                column, width=width, anchor="w"
            )

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical",
            command=self.process_table.yview
        )
        self.process_table.configure(yscrollcommand=scrollbar.set)

        self.process_table.grid(
            row=0, column=0, sticky="nsew", padx=(8, 0), pady=8
        )
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 8), pady=8)

        self.process_count_label = ctk.CTkLabel(
            self.content, text="Loading processes...",
            font=ctk.CTkFont(size=12),
            text_color=self.muted_color
        )
        self.process_count_label.grid(
            row=4, column=0, sticky="w", pady=(12, 0)
        )

        self.sort_column = "cpu"
        self.sort_descending = True
        self.refresh_processes()

    def refresh_processes(self):
        if self.current_page != "Processes":
            return

        try:
            self.process_data = self.process_manager.get_processes()
            self.populate_process_table()
        except (OSError, RuntimeError, psutil.Error) as error:
            messagebox.showerror(
                "Process Manager Error", str(error), parent=self
            )

        self.process_refresh_job = self.after(
            3000, self.refresh_processes
        )

    def populate_process_table(self):
        if not hasattr(self, "process_table"):
            return

        search = self.process_search.get().strip().lower()

        for item in self.process_table.get_children():
            self.process_table.delete(item)

        filtered = [
            process for process in self.process_data
            if search in process["name"].lower()
            or search in str(process["pid"])
        ]

        filtered.sort(
            key=lambda process: process.get(
                self.sort_column, 0
            ),
            reverse=self.sort_descending
        )

        for process in filtered:
            self.process_table.insert(
                "",
                "end",
                iid=str(process["pid"]),
                values=(
                    process["pid"],
                    process["name"],
                    f"{process['cpu_percent']:.1f}",
                    f"{process['memory_mb']:.1f}",
                    process["status"]
                )
            )

        self.process_count_label.configure(
            text=f"Showing {len(filtered)} of {len(self.process_data)} processes"
        )

    def sort_processes(self, column):
        if self.sort_column == column:
            self.sort_descending = not self.sort_descending
        else:
            self.sort_column = column
            self.sort_descending = True

        self.populate_process_table()

    def end_selected_process(self):
        selected = self.process_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Process Selected",
                "Select a process from the table first.",
                parent=self
            )
            return

        pid = int(selected[0])
        process = next(
            (p for p in self.process_data if p["pid"] == pid),
            None
        )

        if process is None:
            messagebox.showwarning(
                "Process Not Found",
                "This process is no longer in the process list.",
                parent=self
            )
            return

        confirmed = messagebox.askyesno(
            "Confirm Process Termination",
            f"Request termination of '{process['name']}' (PID {pid})?\n\n"
            "Unsaved work in that application may be lost. "
            "Avoid terminating Windows system processes.",
            parent=self
        )

        if not confirmed:
            return

        success, message = self.process_manager.terminate_process(pid)

        if success:
            messagebox.showinfo("Process Manager", message, parent=self)
        else:
            messagebox.showerror("Process Manager", message, parent=self)

        self.refresh_processes()

    def show_placeholder(self, page):
        self.clear_content()

        details = {
            "Hardware": (
                "Hardware Information",
                "Review hardware specifications and disk storage."
            ),
            "Alerts": (
                "System Health Alerts",
                "Review warnings and performance thresholds."
            ),
            "Reports": (
                "Performance Reports",
                "Explore saved measurements and diagnostic reports."
            )
        }

        title, description = details[page]

        ctk.CTkLabel(
            self.content, text=title,
            font=ctk.CTkFont(size=27, weight="bold"),
            text_color=self.text_color
        ).pack(anchor="w", pady=(10, 8))

        ctk.CTkLabel(
            self.content, text=description,
            font=ctk.CTkFont(size=13),
            text_color=self.muted_color
        ).pack(anchor="w", pady=(0, 25))

        placeholder = ctk.CTkFrame(
            self.content, fg_color=self.card_color, corner_radius=12
        )
        placeholder.pack(fill="both", expand=True)

        ctk.CTkLabel(
            placeholder, text="MODULE UNDER DEVELOPMENT",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=self.text_color
        ).pack(pady=(100, 10))

        ctk.CTkLabel(
            placeholder,
            text="This section will be implemented in a later stage.",
            font=ctk.CTkFont(size=13),
            text_color=self.muted_color
        ).pack()

    def close_app(self):
        for job in (self.refresh_job, self.process_refresh_job):
            if job is not None:
                self.after_cancel(job)

        self.destroy()


if __name__ == "__main__":
    import psutil

    app = SentinelApp()
    app.mainloop()
