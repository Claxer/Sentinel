import customtkinter as ctk
from tkinter import messagebox


class AlertsPage(ctk.CTkFrame):
    """Dark-themed interface for active alerts and persistent alert history."""

    def __init__(self, parent, alert_manager=None):
        super().__init__(parent, fg_color="#111111", corner_radius=0)

        self.alert_manager = alert_manager
        self.metric_provider = None
        self.active_alerts = []
        self.alert_history = []

        self._build_interface()
        self.refresh_alerts()

    def _build_interface(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 12))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Alerts",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFFFFF",
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header,
            text="Monitor resource thresholds and review recorded events.",
            font=ctk.CTkFont(size=12),
            text_color="#A0A0A0",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        actions = ctk.CTkFrame(header, fg_color="transparent")
        actions.grid(row=0, column=1, rowspan=2, sticky="e")

        ctk.CTkButton(
            actions,
            text="Refresh Alerts",
            command=self.refresh_alerts,
            width=125,
            fg_color="#303030",
            hover_color="#414141",
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            actions,
            text="Clear History",
            command=self.clear_history,
            width=115,
            fg_color="#292929",
            hover_color="#3B3B3B",
            border_width=1,
            border_color="#555555",
        ).pack(side="left")

        self.summary_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.summary_frame.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 12))
        for column in range(3):
            self.summary_frame.grid_columnconfigure(column, weight=1)

        self.active_count_label = self._make_summary_card(
            self.summary_frame, 0, "ACTIVE ALERTS", "0"
        )
        self.critical_count_label = self._make_summary_card(
            self.summary_frame, 1, "CRITICAL", "0"
        )
        self.history_count_label = self._make_summary_card(
            self.summary_frame, 2, "HISTORY EVENTS", "0"
        )

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 24))
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=1)
        body.grid_rowconfigure(3, weight=2)

        ctk.CTkLabel(
            body,
            text="Active Alerts",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF",
        ).grid(row=0, column=0, sticky="w", pady=(4, 8))

        self.active_scroll = ctk.CTkScrollableFrame(
            body, fg_color="#181818", corner_radius=10
        )
        self.active_scroll.grid(row=1, column=0, sticky="nsew", pady=(0, 18))
        self.active_scroll.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            body,
            text="Alert History",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFFFFF",
        ).grid(row=2, column=0, sticky="w", pady=(0, 8))

        self.history_scroll = ctk.CTkScrollableFrame(
            body, fg_color="#181818", corner_radius=10
        )
        self.history_scroll.grid(row=3, column=0, sticky="nsew")
        self.history_scroll.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            self, text="", text_color="#8A8A8A", font=ctk.CTkFont(size=11)
        )
        self.status_label.grid(row=3, column=0, sticky="w", padx=26, pady=(0, 8))

    def _make_summary_card(self, parent, column, title, value):
        card = ctk.CTkFrame(
            parent, fg_color="#1B1B1B", corner_radius=10,
            border_width=1, border_color="#2B2B2B"
        )
        card.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 6, 6), pady=2)
        ctk.CTkLabel(
            card, text=title, text_color="#929292",
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(anchor="w", padx=16, pady=(12, 2))
        value_label = ctk.CTkLabel(
            card, text=value, text_color="#FFFFFF",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        value_label.pack(anchor="w", padx=16, pady=(0, 12))
        return value_label

    def set_metric_provider(self, provider):
        """Set a callable that returns the latest metrics dictionary."""
        self.metric_provider = provider

    def refresh_alerts(self):
        """Refresh active alerts and saved history without crashing the UI."""
        if self.alert_manager is None:
            self._show_empty_state(self.active_scroll, "Alert manager is not connected.")
            self._show_empty_state(self.history_scroll, "No alert manager is available.")
            self.status_label.configure(text="Alert manager unavailable.")
            return

        try:
            if self.metric_provider is not None:
                metrics = self.metric_provider()
                if isinstance(metrics, dict):
                    self.alert_manager.check_metrics(metrics)

            self.active_alerts = self.alert_manager.get_active_alerts() or []
            self.alert_history = self.alert_manager.get_alert_history() or []

            self._render_active_alerts()
            self._render_history()

            critical = sum(
                1 for alert in self.active_alerts
                if str(self._get(alert, "severity", "Warning")).lower() == "critical"
            )
            self.active_count_label.configure(text=str(len(self.active_alerts)))
            self.critical_count_label.configure(text=str(critical))
            self.history_count_label.configure(text=str(len(self.alert_history)))
            self.status_label.configure(text="Alert information refreshed.")
        except Exception as error:
            self.status_label.configure(text=f"Could not refresh alerts: {error}")

    def _render_active_alerts(self):
        self._clear_frame(self.active_scroll)

        if not self.active_alerts:
            self._show_empty_state(self.active_scroll, "No active alerts. System metrics are within configured limits.")
            return

        for index, alert in enumerate(self.active_alerts):
            self._make_alert_card(self.active_scroll, alert, index, active=True)

    def _render_history(self):
        self._clear_frame(self.history_scroll)

        if not self.alert_history:
            self._show_empty_state(self.history_scroll, "No alert history has been recorded yet.")
            return

        for index, alert in enumerate(reversed(self.alert_history)):
            self._make_alert_card(self.history_scroll, alert, index, active=False)

    def _make_alert_card(self, parent, alert, index, active):
        severity = str(self._get(alert, "severity", "Warning")).title()
        critical = severity.lower() == "critical"
        accent = "#D46A6A" if critical else "#D6A85C"

        title = self._first_value(
            alert, ("title", "name", "metric", "type"), "System Alert"
        )
        message = self._first_value(
            alert, ("message", "description", "details"), "Resource threshold triggered."
        )
        timestamp = self._first_value(
            alert, ("timestamp", "time", "created_at", "date"), "Time unavailable"
        )
        value = self._first_value(alert, ("value", "current_value"), None)
        threshold = self._first_value(alert, ("threshold", "limit", "configured_limit"), None)

        card = ctk.CTkFrame(
            parent, fg_color="#202020", corner_radius=8,
            border_width=1, border_color="#303030"
        )
        card.grid(row=index, column=0, sticky="ew", padx=8, pady=5)
        card.grid_columnconfigure(0, weight=1)

        top = ctk.CTkFrame(card, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 2))
        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            top, text=str(title), text_color="#FFFFFF",
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            top, text=severity.upper(), text_color=accent,
            font=ctk.CTkFont(size=10, weight="bold")
        ).grid(row=0, column=1, sticky="e")

        ctk.CTkLabel(
            card, text=str(message), text_color="#C0C0C0",
            font=ctk.CTkFont(size=11), justify="left", wraplength=850
        ).grid(row=1, column=0, sticky="w", padx=12, pady=(2, 4))

        details = f"Time: {timestamp}"
        if value is not None:
            details += f"   |   Current: {value}"
        if threshold is not None:
            details += f"   |   Threshold: {threshold}"

        ctk.CTkLabel(
            card, text=details, text_color="#858585",
            font=ctk.CTkFont(size=10)
        ).grid(row=2, column=0, sticky="w", padx=12, pady=(0, 10))

    def clear_history(self):
        if self.alert_manager is None:
            return

        if not messagebox.askyesno(
            "Clear Alert History",
            "Delete the saved alert-history events? Active alerts will not be changed.",
            parent=self.winfo_toplevel(),
        ):
            return

        try:
            self.alert_manager.clear_history()
            self.refresh_alerts()
            self.status_label.configure(text="Alert history cleared.")
        except Exception as error:
            messagebox.showerror(
                "Clear History Failed",
                f"Could not clear alert history:\n{error}",
                parent=self.winfo_toplevel(),
            )

    @staticmethod
    def _get(item, key, default=None):
        if isinstance(item, dict):
            return item.get(key, default)
        return getattr(item, key, default)

    @classmethod
    def _first_value(cls, item, keys, default):
        for key in keys:
            value = cls._get(item, key)
            if value not in (None, ""):
                return value
        return default

    @staticmethod
    def _clear_frame(frame):
        for child in frame.winfo_children():
            child.destroy()

    @staticmethod
    def _show_empty_state(frame, message):
        ctk.CTkLabel(
            frame,
            text=message,
            text_color="#858585",
            font=ctk.CTkFont(size=12),
            wraplength=800,
        ).grid(row=0, column=0, sticky="w", padx=14, pady=14)
