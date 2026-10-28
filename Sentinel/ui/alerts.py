import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime


class AlertsPage(ctk.CTkFrame):
    def __init__(self, parent, alert_manager=None):
        super().__init__(parent, fg_color="#151515")

        self.alert_manager = alert_manager
        self.metric_provider = None
        self.active_alerts = []
        self.alert_history = []

        self.build_ui()
        self.refresh_alerts()

    # ============================================================
    # USER INTERFACE
    # ============================================================

    def build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(22, 12))

        ctk.CTkLabel(
            header,
            text="Alerts",
            font=("Segoe UI", 27, "bold"),
            text_color="#F2F2F2"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Monitor resource warnings and review previous alert events.",
            font=("Segoe UI", 12),
            text_color="#999999"
        ).pack(anchor="w", pady=(4, 0))

        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=24, pady=(4, 14))

        ctk.CTkButton(
            toolbar,
            text="Refresh Alerts",
            width=130,
            fg_color="#303030",
            hover_color="#414141",
            command=self.refresh_alerts
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            toolbar,
            text="Clear History",
            width=120,
            fg_color="#612B2B",
            hover_color="#813737",
            command=self.clear_history
        ).pack(side="left")

        self.status_label = ctk.CTkLabel(
            toolbar,
            text="",
            font=("Segoe UI", 11),
            text_color="#999999"
        )
        self.status_label.pack(side="right")

        # Active alerts
        ctk.CTkLabel(
            self,
            text="ACTIVE ALERTS",
            font=("Segoe UI", 13, "bold"),
            text_color="#E6E6E6"
        ).pack(anchor="w", padx=24, pady=(4, 8))

        self.active_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#1D1D1D",
            corner_radius=10,
            height=200
        )
        self.active_frame.pack(
            fill="x",
            padx=24,
            pady=(0, 18)
        )

        # Alert history
        history_header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        history_header.pack(
            fill="x",
            padx=24,
            pady=(0, 8)
        )

        ctk.CTkLabel(
            history_header,
            text="ALERT HISTORY",
            font=("Segoe UI", 13, "bold"),
            text_color="#E6E6E6"
        ).pack(side="left")

        self.history_count_label = ctk.CTkLabel(
            history_header,
            text="0 events",
            font=("Segoe UI", 11),
            text_color="#999999"
        )
        self.history_count_label.pack(side="right")

        self.history_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#1D1D1D",
            corner_radius=10
        )
        self.history_frame.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=(0, 22)
        )

    # ============================================================
    # METRIC PROVIDER
    # ============================================================

    def set_metric_provider(self, provider):
        """Set a callback that returns the latest system metrics."""
        self.metric_provider = provider

    # ============================================================
    # REFRESH ALERTS
    # ============================================================

    def refresh_alerts(self):
        if self.alert_manager is None:
            self.show_active_empty(
                "Alert manager is not connected."
            )
            self.show_history_empty(
                "Alert history is unavailable."
            )
            self.status_label.configure(
                text="Alert manager unavailable"
            )
            return

        # Ask the app for current metrics when a provider is available.
        if self.metric_provider is not None:
            try:
                metrics = self.metric_provider()

                if isinstance(metrics, dict):
                    self.alert_manager.check_metrics(metrics)

            except Exception as error:
                self.status_label.configure(
                    text=f"Metric update failed: {error}"
                )

        try:
            self.active_alerts = (
                self.alert_manager.get_active_alerts() or []
            )
        except Exception as error:
            self.active_alerts = []
            self.status_label.configure(
                text=f"Could not load active alerts: {error}"
            )

        try:
            self.alert_history = (
                self.alert_manager.get_alert_history() or []
            )
        except Exception as error:
            self.alert_history = []
            self.status_label.configure(
                text=f"Could not load history: {error}"
            )

        self.render_active_alerts()
        self.render_alert_history()

        self.status_label.configure(
            text=f"Last refreshed: {datetime.now().strftime('%H:%M:%S')}"
        )

    # ============================================================
    # ACTIVE ALERTS
    # ============================================================

    def render_active_alerts(self):
        for widget in self.active_frame.winfo_children():
            widget.destroy()

        if not self.active_alerts:
            self.show_active_empty(
                "No active alerts. System resource usage is within limits."
            )
            return

        for alert in self.active_alerts:
            self.create_alert_card(
                self.active_frame,
                alert,
                is_history=False
            )

    def show_active_empty(self, message):
        for widget in self.active_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.active_frame,
            text=message,
            text_color="#999999",
            font=("Segoe UI", 12)
        ).pack(padx=15, pady=24)

    # ============================================================
    # ALERT HISTORY
    # ============================================================

    def render_alert_history(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        self.history_count_label.configure(
            text=f"{len(self.alert_history)} events"
        )

        if not self.alert_history:
            self.show_history_empty(
                "No alert events have been recorded yet."
            )
            return

        # Newest events appear first.
        for alert in reversed(self.alert_history):
            self.create_alert_card(
                self.history_frame,
                alert,
                is_history=True
            )

    def show_history_empty(self, message):
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.history_frame,
            text=message,
            text_color="#999999",
            font=("Segoe UI", 12)
        ).pack(padx=15, pady=24)

    # ============================================================
    # ALERT CARD
    # ============================================================

    def create_alert_card(self, parent, alert, is_history=False):
        severity = str(alert.get("severity", "Warning")).title()

        if severity == "Critical":
            severity_color = "#FF6666"
        else:
            severity_color = "#E5B567"

        card = ctk.CTkFrame(
            parent,
            fg_color="#262626",
            corner_radius=8,
            border_width=1,
            border_color="#353535"
        )
        card.pack(fill="x", padx=8, pady=5)

        top_row = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        top_row.pack(
            fill="x",
            padx=12,
            pady=(10, 4)
        )

        name = alert.get(
            "name",
            alert.get("metric", "System Alert")
        )

        ctk.CTkLabel(
            top_row,
            text=str(name),
            font=("Segoe UI", 13, "bold"),
            text_color="#F0F0F0"
        ).pack(side="left")

        ctk.CTkLabel(
            top_row,
            text=severity.upper(),
            font=("Segoe UI", 10, "bold"),
            text_color=severity_color
        ).pack(side="right")

        message = alert.get(
            "message",
            "A system resource threshold was exceeded."
        )

        ctk.CTkLabel(
            card,
            text=str(message),
            font=("Segoe UI", 11),
            text_color="#BBBBBB",
            wraplength=850,
            justify="left"
        ).pack(
            anchor="w",
            padx=12,
            pady=(0, 6)
        )

        value = alert.get("value")
        threshold = alert.get("threshold")
        timestamp = alert.get("timestamp", "Unknown time")

        if isinstance(timestamp, (int, float)):
            try:
                timestamp = datetime.fromtimestamp(
                    timestamp
                ).strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, OSError, OverflowError):
                timestamp = str(timestamp)

        details = []

        if value is not None:
            details.append(f"Value: {value}%")

        if threshold is not None:
            details.append(f"Limit: {threshold}%")

        details.append(f"Time: {timestamp}")

        if is_history:
            details.append("Recorded event")

        ctk.CTkLabel(
            card,
            text="  |  ".join(details),
            font=("Segoe UI", 10),
            text_color="#888888"
        ).pack(
            anchor="w",
            padx=12,
            pady=(0, 10)
        )

    # ============================================================
    # CLEAR HISTORY
    # ============================================================

    def clear_history(self):
        if self.alert_manager is None:
            messagebox.showerror(
                "Alerts",
                "The alert manager is not available.",
                parent=self
            )
            return

        if not self.alert_history:
            messagebox.showinfo(
                "Alert History",
                "There is no alert history to clear.",
                parent=self
            )
            return

        confirmed = messagebox.askyesno(
            "Clear Alert History",
            "Are you sure you want to permanently clear saved "
            "alert history? Active alerts will not be removed.",
            parent=self
        )

        if not confirmed:
            return

        try:
            self.alert_manager.clear_history()
            self.refresh_alerts()

            messagebox.showinfo(
                "Alert History",
                "Saved alert history has been cleared.",
                parent=self
            )

        except Exception as error:
            messagebox.showerror(
                "Clear History Failed",
                f"Could not clear alert history:\n\n{error}",
                parent=self
            )
