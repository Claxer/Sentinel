import customtkinter as ctk

from core.alert_manager import AlertManager


class AlertsPage(ctk.CTkFrame):
    def __init__(self, parent, alert_manager=None):
        super().__init__(parent, fg_color="transparent")

        self.alert_manager = alert_manager or AlertManager()
        self.metric_provider = None

        self.create_interface()
        self.refresh_alerts()

    def create_interface(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))

        title_area = ctk.CTkFrame(
            header, fg_color="transparent"
        )
        title_area.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            title_area,
            text="System Alerts",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="#F2F2F2"
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_area,
            text="Monitor resource warnings and system conditions",
            font=ctk.CTkFont(size=12),
            text_color="#A0A0A0"
        ).pack(anchor="w", pady=(4, 0))

        ctk.CTkButton(
            header,
            text="Refresh",
            width=100,
            command=self.refresh_alerts,
            fg_color="#343434",
            hover_color="#484848"
        ).pack(side="right")

        self.scroll_area = ctk.CTkScrollableFrame(
            self, fg_color="transparent"
        )
        self.scroll_area.pack(
            fill="both", expand=True, padx=20, pady=(0, 20)
        )

        self.summary_frame = ctk.CTkFrame(
            self.scroll_area, fg_color="transparent"
        )
        self.summary_frame.pack(fill="x", pady=(5, 15))

        self.summary_labels = {}

        for index, (key, heading) in enumerate([
            ("active", "Active Alerts"),
            ("critical", "Critical"),
            ("warnings", "Warnings")
        ]):
            self.summary_frame.grid_columnconfigure(
                index, weight=1
            )

            card = ctk.CTkFrame(
                self.summary_frame,
                fg_color="#202020",
                corner_radius=10,
                height=90
            )
            card.grid(
                row=0, column=index, sticky="nsew",
                padx=(0 if index == 0 else 5, 5)
            )
            card.grid_propagate(False)

            ctk.CTkLabel(
                card,
                text=heading,
                text_color="#A0A0A0",
                font=ctk.CTkFont(size=12)
            ).pack(anchor="w", padx=12, pady=(12, 3))

            number = ctk.CTkLabel(
                card,
                text="0",
                text_color="#F2F2F2",
                font=ctk.CTkFont(size=24, weight="bold")
            )
            number.pack(anchor="w", padx=12)

            self.summary_labels[key] = number

        ctk.CTkLabel(
            self.scroll_area,
            text="Active Alerts",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#EEEEEE"
        ).pack(anchor="w", pady=(5, 8))

        self.active_frame = ctk.CTkFrame(
            self.scroll_area,
            fg_color="#202020",
            corner_radius=10
        )
        self.active_frame.pack(fill="x", pady=(0, 18))

        ctk.CTkLabel(
            self.scroll_area,
            text="Alert History",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#EEEEEE"
        ).pack(anchor="w", pady=(5, 8))

        history_header = ctk.CTkFrame(
            self.scroll_area, fg_color="transparent"
        )
        history_header.pack(fill="x", pady=(0, 8))

        self.history_count = ctk.CTkLabel(
            history_header,
            text="Recent alert events",
            text_color="#A0A0A0"
        )
        self.history_count.pack(side="left")

        ctk.CTkButton(
            history_header,
            text="Clear History",
            width=110,
            fg_color="#343434",
            hover_color="#484848",
            command=self.clear_history
        ).pack(side="right")

        self.history_frame = ctk.CTkFrame(
            self.scroll_area,
            fg_color="#202020",
            corner_radius=10
        )
        self.history_frame.pack(fill="x", pady=(0, 15))

        self.status_label = ctk.CTkLabel(
            self.scroll_area,
            text="Ready",
            text_color="#A0A0A0",
            font=ctk.CTkFont(size=11)
        )
        self.status_label.pack(anchor="w", pady=(0, 10))

    def set_metric_provider(self, provider):
        """Set a callable that returns the latest system metrics."""
        self.metric_provider = provider

    def refresh_alerts(self):
        if self.metric_provider is not None:
            try:
                metrics = self.metric_provider()
                self.alert_manager.check_metrics(metrics)
            except Exception as error:
                self.status_label.configure(
                    text=f"Unable to check system metrics: {error}",
                    text_color="#E07070"
                )
                return

        self.render_alerts()

    def render_alerts(self):
        active = self.alert_manager.get_active_alerts()
        history = self.alert_manager.get_alert_history()

        critical_count = sum(
            1 for alert in active
            if alert["severity"] == "Critical"
        )
        warning_count = sum(
            1 for alert in active
            if alert["severity"] == "Warning"
        )

        self.summary_labels["active"].configure(
            text=str(len(active))
        )
        self.summary_labels["critical"].configure(
            text=str(critical_count)
        )
        self.summary_labels["warnings"].configure(
            text=str(warning_count)
        )

        self.render_active_alerts(active)
        self.render_history(history)

        self.status_label.configure(
            text="Alert information updated.",
            text_color="#A0A0A0"
        )

    def render_active_alerts(self, active):
        for widget in self.active_frame.winfo_children():
            widget.destroy()

        if not active:
            ctk.CTkLabel(
                self.active_frame,
                text="No active alerts. Your monitored metrics are within their configured limits.",
                text_color="#A0A0A0",
                wraplength=650,
                justify="left"
            ).pack(anchor="w", padx=15, pady=18)
            return

        for alert in active:
            color = (
                "#E07070"
                if alert["severity"] == "Critical"
                else "#E0B060"
            )

            card = ctk.CTkFrame(
                self.active_frame,
                fg_color="#292929",
                corner_radius=8
            )
            card.pack(fill="x", padx=10, pady=6)

            top = ctk.CTkFrame(
                card, fg_color="transparent"
            )
            top.pack(fill="x", padx=12, pady=(10, 3))

            ctk.CTkLabel(
                top,
                text=alert["title"],
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#F0F0F0"
            ).pack(side="left")

            ctk.CTkLabel(
                top,
                text=alert["severity"].upper(),
                text_color=color,
                font=ctk.CTkFont(size=11, weight="bold")
            ).pack(side="right")

            ctk.CTkLabel(
                card,
                text=(
                    f'{alert["description"]} '
                    f'Current reading: {alert["value"]}% '
                    f'(limit: {alert["limit"]}%).'
                ),
                text_color="#BBBBBB",
                wraplength=650,
                justify="left"
            ).pack(anchor="w", padx=12, pady=(2, 5))

            ctk.CTkLabel(
                card,
                text=f'First detected: {alert["timestamp"]}',
                text_color="#888888",
                font=ctk.CTkFont(size=10)
            ).pack(anchor="w", padx=12, pady=(0, 10))

    def render_history(self, history):
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        self.history_count.configure(
            text=f"{len(history)} recorded alert events"
        )

        if not history:
            ctk.CTkLabel(
                self.history_frame,
                text="No alert events have been recorded yet.",
                text_color="#A0A0A0"
            ).pack(anchor="w", padx=15, pady=18)
            return

        for alert in history:
            row = ctk.CTkFrame(
                self.history_frame,
                fg_color="transparent"
            )
            row.pack(fill="x", padx=12, pady=8)

            ctk.CTkLabel(
                row,
                text=alert["title"],
                text_color="#EEEEEE",
                anchor="w"
            ).pack(side="left", fill="x", expand=True)

            ctk.CTkLabel(
                row,
                text=f'{alert["value"]}%',
                text_color="#BBBBBB",
                width=55
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=alert["timestamp"],
                text_color="#888888",
                font=ctk.CTkFont(size=10)
            ).pack(side="right")

    def clear_history(self):
        self.alert_manager.clear_history()
        self.render_alerts()
