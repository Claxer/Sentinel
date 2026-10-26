import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import datetime

from core.report_manager import ReportManager


class ReportsPage(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        system_monitor,
        process_manager,
        alert_manager
    ):
        super().__init__(parent, fg_color="#111111")

        self.system_monitor = system_monitor
        self.process_manager = process_manager
        self.alert_manager = alert_manager
        self.report_manager = ReportManager()

        self.create_interface()

    def create_interface(self):
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=28,
            pady=(25, 10)
        )

        ctk.CTkLabel(
            header,
            text="Reports",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Generate and export system information",
            font=ctk.CTkFont(size=13),
            text_color="#999999"
        ).pack(anchor="w", pady=(5, 0))

        self.status_label = ctk.CTkLabel(
            self,
            text="Choose a report to export.",
            text_color="#AAAAAA",
            font=ctk.CTkFont(size=12),
            wraplength=850,
            justify="left"
        )
        self.status_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=30,
            pady=(5, 15)
        )

        report_container = ctk.CTkFrame(
            self,
            fg_color="#1B1B1B",
            corner_radius=12
        )
        report_container.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=28,
            pady=10
        )
        report_container.grid_columnconfigure(0, weight=1)

        reports = [
            (
                "System Metrics Report",
                "Export CPU, RAM, disk, network, and other available metrics.",
                "Export System Report",
                self.export_system_report
            ),
            (
                "Process Report",
                "Export information about currently running processes.",
                "Export Process Report",
                self.export_process_report
            ),
            (
                "Active Alerts Report",
                "Export alerts that are currently active.",
                "Export Active Alerts",
                self.export_active_alerts
            ),
            (
                "Alert History Report",
                "Export alert events recorded during this session.",
                "Export Alert History",
                self.export_alert_history
            )
        ]

        for index, report in enumerate(reports):
            title, description, button_text, command = report

            card = ctk.CTkFrame(
                report_container,
                fg_color="#242424",
                corner_radius=10
            )
            card.grid(
                row=index,
                column=0,
                sticky="ew",
                padx=14,
                pady=(14 if index == 0 else 6, 6)
            )
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#FFFFFF"
            ).grid(
                row=0,
                column=0,
                sticky="w",
                padx=16,
                pady=(14, 4)
            )

            ctk.CTkLabel(
                card,
                text=description,
                font=ctk.CTkFont(size=12),
                text_color="#AAAAAA",
                wraplength=550,
                justify="left"
            ).grid(
                row=1,
                column=0,
                sticky="w",
                padx=16,
                pady=(0, 14)
            )

            ctk.CTkButton(
                card,
                text=button_text,
                width=190,
                height=34,
                fg_color="#3A3A3A",
                hover_color="#505050",
                text_color="#FFFFFF",
                command=command
            ).grid(
                row=0,
                column=1,
                rowspan=2,
                padx=16,
                pady=12
            )

        ctk.CTkLabel(
            self,
            text=(
                "Reports are exported as CSV files that can be opened "
                "in spreadsheet applications. Alert history is currently "
                "stored in memory and is not retained after Sentinel closes."
            ),
            font=ctk.CTkFont(size=11),
            text_color="#777777",
            wraplength=850,
            justify="left"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=30,
            pady=20
        )

    def choose_save_location(self, title, default_name):
        return filedialog.asksaveasfilename(
            title=title,
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=[("CSV files", "*.csv")]
        )

    def export_file(self, title, default_name, export_function, data):
        file_path = self.choose_save_location(title, default_name)

        if not file_path:
            self.status_label.configure(text="Export cancelled.")
            return

        try:
            export_function(file_path, data)

            self.status_label.configure(
                text=f"Report saved: {file_path}",
                text_color="#8BCF9B"
            )

            messagebox.showinfo(
                "Export Successful",
                f"Your report was saved successfully:\n\n{file_path}",
                parent=self
            )

        except (OSError, ValueError, TypeError, KeyError) as error:
            self.status_label.configure(
                text="Export failed. Please try again.",
                text_color="#FF7777"
            )

            messagebox.showerror(
                "Export Failed",
                f"Could not export the report.\n\n{error}",
                parent=self
            )

    def export_system_report(self):
        try:
            metrics = self.system_monitor.get_metrics()

            filename = (
                "sentinel_system_"
                + datetime.now().strftime("%Y%m%d_%H%M%S")
                + ".csv"
            )

            self.export_file(
                "Save System Report",
                filename,
                self.report_manager.export_system_report,
                metrics
            )

        except Exception as error:
            messagebox.showerror(
                "System Report Error",
                str(error),
                parent=self
            )

    def export_process_report(self):
        try:
            processes = self.process_manager.get_processes()

            filename = (
                "sentinel_processes_"
                + datetime.now().strftime("%Y%m%d_%H%M%S")
                + ".csv"
            )

            self.export_file(
                "Save Process Report",
                filename,
                self.report_manager.export_process_report,
                processes
            )

        except Exception as error:
            messagebox.showerror(
                "Process Report Error",
                str(error),
                parent=self
            )

    def export_active_alerts(self):
        try:
            alerts = self.alert_manager.get_active_alerts()

            filename = (
                "sentinel_active_alerts_"
                + datetime.now().strftime("%Y%m%d_%H%M%S")
                + ".csv"
            )

            self.export_file(
                "Save Active Alerts Report",
                filename,
                self.report_manager.export_alert_report,
                alerts
            )

        except Exception as error:
            messagebox.showerror(
                "Active Alerts Error",
                str(error),
                parent=self
            )

    def export_alert_history(self):
        try:
            alerts = self.alert_manager.get_alert_history()

            filename = (
                "sentinel_alert_history_"
                + datetime.now().strftime("%Y%m%d_%H%M%S")
                + ".csv"
            )

            self.export_file(
                "Save Alert History Report",
                filename,
                self.report_manager.export_alert_report,
                alerts
            )

        except Exception as error:
            messagebox.showerror(
                "Alert History Error",
                str(error),
                parent=self
            )
