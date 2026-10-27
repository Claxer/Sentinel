import customtkinter as ctk
from tkinter import messagebox

from core.settings_manager import SettingsManager


class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, settings_manager=None):
        super().__init__(parent, fg_color="#111111")

        self.settings_manager = (
            settings_manager
            if settings_manager is not None
            else SettingsManager()
        )

        self.setting_variables = {}

        self.create_interface()
        self.load_current_settings()

    # =========================
    # INTERFACE
    # =========================

    def create_interface(self):
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=28,
            pady=(25, 15)
        )

        ctk.CTkLabel(
            header,
            text="Settings",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Configure monitoring behavior and resource alert thresholds",
            font=ctk.CTkFont(size=13),
            text_color="#999999"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        self.status_label = ctk.CTkLabel(
            self,
            text="Adjust your preferences and save your changes.",
            font=ctk.CTkFont(size=12),
            text_color="#AAAAAA",
            wraplength=800,
            justify="left"
        )
        self.status_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=30,
            pady=(0, 10)
        )

        settings_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )
        settings_container.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=22,
            pady=(0, 10)
        )
        self.grid_rowconfigure(2, weight=1)

        # Resource alert settings
        self.create_section(
            settings_container,
            row=0,
            title="Resource Alert Thresholds",
            description=(
                "Choose the usage percentage at which Sentinel "
                "should trigger a resource alert."
            ),
            settings=[
                (
                    "cpu_limit",
                    "CPU Usage Threshold",
                    "Trigger an alert when CPU usage reaches this percentage.",
                    1,
                    100,
                    "%"
                ),
                (
                    "ram_limit",
                    "Memory Usage Threshold",
                    "Trigger an alert when RAM usage reaches this percentage.",
                    1,
                    100,
                    "%"
                ),
                (
                    "disk_limit",
                    "Disk Usage Threshold",
                    "Trigger an alert when disk usage reaches this percentage.",
                    1,
                    100,
                    "%"
                )
            ]
        )

        # Monitoring intervals
        self.create_section(
            settings_container,
            row=1,
            title="Monitoring Intervals",
            description=(
                "Control how frequently Sentinel refreshes "
                "the Dashboard and Process Manager."
            ),
            settings=[
                (
                    "dashboard_refresh_seconds",
                    "Dashboard Refresh Interval",
                    "How often system metrics and graphs update.",
                    1,
                    60,
                    "seconds"
                ),
                (
                    "process_refresh_seconds",
                    "Process Refresh Interval",
                    "How often the running process list refreshes.",
                    2,
                    300,
                    "seconds"
                )
            ]
        )

        # Bottom actions
        actions = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        actions.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=28,
            pady=(5, 20)
        )

        ctk.CTkButton(
            actions,
            text="Save Settings",
            width=150,
            height=38,
            fg_color="#3A3A3A",
            hover_color="#505050",
            text_color="#FFFFFF",
            command=self.save_settings
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ctk.CTkButton(
            actions,
            text="Reset to Defaults",
            width=150,
            height=38,
            fg_color="#242424",
            hover_color="#383838",
            text_color="#DDDDDD",
            command=self.reset_settings
        ).pack(side="left")

    def create_section(
        self,
        parent,
        row,
        title,
        description,
        settings
    ):
        section = ctk.CTkFrame(
            parent,
            fg_color="#1B1B1B",
            corner_radius=12
        )
        section.grid(
            row=row,
            column=0,
            sticky="ew",
            padx=6,
            pady=7
        )
        section.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            section,
            text=title,
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#FFFFFF"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=18,
            pady=(16, 3)
        )

        ctk.CTkLabel(
            section,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color="#999999",
            wraplength=650,
            justify="left"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=18,
            pady=(0, 10)
        )

        for index, setting in enumerate(settings, start=2):
            key, label, help_text, minimum, maximum, unit = setting

            row_frame = ctk.CTkFrame(
                section,
                fg_color="#242424",
                corner_radius=8
            )
            row_frame.grid(
                row=index,
                column=0,
                sticky="ew",
                padx=12,
                pady=5
            )
            row_frame.grid_columnconfigure(0, weight=1)

            text_frame = ctk.CTkFrame(
                row_frame,
                fg_color="transparent"
            )
            text_frame.grid(
                row=0,
                column=0,
                sticky="ew",
                padx=12,
                pady=10
            )

            ctk.CTkLabel(
                text_frame,
                text=label,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="#EEEEEE"
            ).pack(anchor="w")

            ctk.CTkLabel(
                text_frame,
                text=help_text,
                font=ctk.CTkFont(size=11),
                text_color="#999999",
                wraplength=480,
                justify="left"
            ).pack(
                anchor="w",
                pady=(3, 0)
            )

            variable = ctk.StringVar()
            self.setting_variables[key] = variable

            input_frame = ctk.CTkFrame(
                row_frame,
                fg_color="transparent"
            )
            input_frame.grid(
                row=0,
                column=1,
                padx=12,
                pady=10
            )

            entry = ctk.CTkEntry(
                input_frame,
                width=85,
                height=32,
                textvariable=variable,
                justify="center"
            )
            entry.pack(side="left")

            ctk.CTkLabel(
                input_frame,
                text=unit,
                font=ctk.CTkFont(size=11),
                text_color="#AAAAAA",
                width=55
            ).pack(
                side="left",
                padx=(6, 0)
            )

            ctk.CTkLabel(
                row_frame,
                text=f"{minimum}–{maximum}",
                font=ctk.CTkFont(size=10),
                text_color="#777777"
            ).grid(
                row=0,
                column=2,
                padx=(0, 12)
            )

    # =========================
    # LOAD SETTINGS
    # =========================

    def load_current_settings(self):
        settings = self.settings_manager.get_settings()

        for key, variable in self.setting_variables.items():
            variable.set(str(settings.get(key, "")))

    # =========================
    # SAVE SETTINGS
    # =========================

    def save_settings(self):
        new_settings = {}

        for key, variable in self.setting_variables.items():
            raw_value = variable.get().strip()

            try:
                if not raw_value:
                    raise ValueError(
                        f"{key.replace('_', ' ').title()} cannot be empty."
                    )

                new_settings[key] = int(raw_value)

            except ValueError:
                messagebox.showerror(
                    "Invalid Setting",
                    (
                        f"Please enter a whole number for "
                        f"{key.replace('_', ' ').title()}."
                    ),
                    parent=self
                )
                return

        if self.settings_manager.update_settings(new_settings):
            self.status_label.configure(
                text="Settings saved successfully.",
                text_color="#8BCF9B"
            )

            messagebox.showinfo(
                "Settings Saved",
                (
                    "Your settings have been saved.\n\n"
                    "Changes to monitoring intervals and alert "
                    "thresholds take effect after they are connected "
                    "to the corresponding monitoring components."
                ),
                parent=self
            )

            self.load_current_settings()

        else:
            self.status_label.configure(
                text="Settings could not be saved. Check the values and file permissions.",
                text_color="#FF7777"
            )

            messagebox.showerror(
                "Save Failed",
                (
                    "Sentinel could not save your settings. "
                    "Check that all values are within the allowed ranges "
                    "and that the project folder is writable."
                ),
                parent=self
            )

    # =========================
    # RESET SETTINGS
    # =========================

    def reset_settings(self):
        confirmed = messagebox.askyesno(
            "Reset Settings",
            (
                "Restore all settings to their default values?\n\n"
                "CPU threshold: 85%\n"
                "RAM threshold: 85%\n"
                "Disk threshold: 90%\n"
                "Dashboard refresh: 2 seconds\n"
                "Process refresh: 5 seconds"
            ),
            parent=self
        )

        if not confirmed:
            return

        if self.settings_manager.reset_settings():
            self.load_current_settings()

            self.status_label.configure(
                text="Default settings restored and saved.",
                text_color="#8BCF9B"
            )

            messagebox.showinfo(
                "Settings Reset",
                "Sentinel's default settings have been restored.",
                parent=self
            )

        else:
            self.status_label.configure(
                text="Could not reset settings.",
                text_color="#FF7777"
            )

            messagebox.showerror(
                "Reset Failed",
                "Sentinel could not save the default settings.",
                parent=self
            )
