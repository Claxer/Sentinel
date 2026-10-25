import customtkinter as ctk
from tkinter import ttk

from core.hardware_info import HardwareInfo


class HardwarePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.hardware = HardwareInfo()
        self.cards = {}
        self.value_labels = {}

        self.configure(fg_color="transparent")
        self.create_interface()
        self.refresh_data()

    def create_interface(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))

        title_area = ctk.CTkFrame(
            header, fg_color="transparent"
        )
        title_area.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            title_area,
            text="Hardware Overview",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color="#F2F2F2"
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_area,
            text="System specifications and device diagnostics",
            font=ctk.CTkFont(size=12),
            text_color="#A0A0A0"
        ).pack(anchor="w", pady=(4, 0))

        ctk.CTkButton(
            header,
            text="Refresh Data",
            width=120,
            command=self.refresh_data,
            fg_color="#343434",
            hover_color="#484848"
        ).pack(side="right", padx=(10, 0))

        self.scroll_area = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.scroll_area.pack(
            fill="both", expand=True, padx=20, pady=(0, 20)
        )

        self.create_summary_cards()
        self.create_section_title("Processor")
        self.cpu_frame = ctk.CTkFrame(
            self.scroll_area,
            fg_color="#202020",
            corner_radius=10
        )
        self.cpu_frame.pack(fill="x", pady=(5, 15))

        self.create_section_title("Memory")
        self.memory_frame = ctk.CTkFrame(
            self.scroll_area,
            fg_color="#202020",
            corner_radius=10
        )
        self.memory_frame.pack(fill="x", pady=(5, 15))

        self.create_section_title("Storage Drives")
        self.disk_frame = ctk.CTkFrame(
            self.scroll_area,
            fg_color="#202020",
            corner_radius=10
        )
        self.disk_frame.pack(fill="x", pady=(5, 15))

        self.create_section_title("Network Adapters")
        self.network_frame = ctk.CTkFrame(
            self.scroll_area,
            fg_color="#202020",
            corner_radius=10
        )
        self.network_frame.pack(fill="x", pady=(5, 15))

        self.create_section_title("Battery and Temperature")
        self.extra_frame = ctk.CTkFrame(
            self.scroll_area,
            fg_color="#202020",
            corner_radius=10
        )
        self.extra_frame.pack(fill="x", pady=(5, 15))

        self.create_section_title("Operating System")
        self.system_frame = ctk.CTkFrame(
            self.scroll_area,
            fg_color="#202020",
            corner_radius=10
        )
        self.system_frame.pack(fill="x", pady=(5, 15))

        self.status_label = ctk.CTkLabel(
            self.scroll_area,
            text="Ready",
            text_color="#999999",
            font=ctk.CTkFont(size=11)
        )
        self.status_label.pack(anchor="w", pady=(0, 10))

    def create_summary_cards(self):
        container = ctk.CTkFrame(
            self.scroll_area, fg_color="transparent"
        )
        container.pack(fill="x", pady=(5, 15))

        card_data = [
            ("CPU", "cpu"),
            ("RAM", "ram"),
            ("Storage", "storage"),
            ("Uptime", "uptime"),
        ]

        for index, (heading, key) in enumerate(card_data):
            container.grid_columnconfigure(index, weight=1)

            card = ctk.CTkFrame(
                container,
                fg_color="#202020",
                corner_radius=10,
                height=100
            )
            card.grid(
                row=0,
                column=index,
                sticky="nsew",
                padx=(0 if index == 0 else 5, 5)
            )
            card.grid_propagate(False)

            ctk.CTkLabel(
                card,
                text=heading,
                text_color="#A0A0A0",
                font=ctk.CTkFont(size=12)
            ).pack(anchor="w", padx=12, pady=(13, 5))

            value = ctk.CTkLabel(
                card,
                text="Loading...",
                text_color="#FFFFFF",
                font=ctk.CTkFont(size=17, weight="bold")
            )
            value.pack(anchor="w", padx=12)

            self.value_labels[key] = value

    def create_section_title(self, title):
        ctk.CTkLabel(
            self.scroll_area,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#EEEEEE"
        ).pack(anchor="w", pady=(5, 2))

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def add_info_row(self, parent, label, value):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            row,
            text=label,
            width=165,
            anchor="w",
            text_color="#A0A0A0"
        ).pack(side="left")

        ctk.CTkLabel(
            row,
            text=str(value),
            anchor="w",
            justify="left",
            wraplength=600,
            text_color="#F0F0F0"
        ).pack(side="left", fill="x", expand=True)

    def create_table(self, parent, columns, headings):
        table_frame = ctk.CTkFrame(
            parent, fg_color="transparent"
        )
        table_frame.pack(
            fill="x", expand=True, padx=10, pady=10
        )

        style = ttk.Style()

        style.configure(
            "Sentinel.Treeview",
            background="#202020",
            foreground="#EAEAEA",
            fieldbackground="#202020",
            rowheight=29,
            borderwidth=0
        )
        style.configure(
            "Sentinel.Treeview.Heading",
            background="#343434",
            foreground="#FFFFFF",
            font=("Segoe UI", 10, "bold")
        )
        style.map(
            "Sentinel.Treeview",
            background=[("selected", "#454545")],
            foreground=[("selected", "#FFFFFF")]
        )

        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Sentinel.Treeview",
            height=4
        )

        for column, heading in zip(columns, headings):
            table.heading(column, text=heading)
            table.column(column, width=120, minwidth=80)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=table.yview
        )
        table.configure(yscrollcommand=scrollbar.set)

        table.pack(side="left", fill="x", expand=True)
        scrollbar.pack(side="right", fill="y")

        return table

    def refresh_data(self):
        try:
            data = self.hardware.get_all_info()

            self.update_summary(data)
            self.update_cpu(data["cpu"])
            self.update_memory(data["memory"])
            self.update_disks(data["disks"])
            self.update_network(data["network"])
            self.update_extra(
                data["battery"], data["temperature"]
            )
            self.update_system(data["system"])

            self.status_label.configure(
                text="Hardware information refreshed successfully."
            )

        except Exception as error:
            self.status_label.configure(
                text=f"Unable to refresh hardware information: {error}",
                text_color="#E07070"
            )

    def update_summary(self, data):
        cpu = data["cpu"]
        memory = data["memory"]
        disks = data["disks"]
        system = data["system"]

        total_storage = sum(
            disk["total_gb"] for disk in disks
        )

        self.value_labels["cpu"].configure(
            text=f'{cpu["usage_percent"]:.0f}% usage'
        )
        self.value_labels["ram"].configure(
            text=f'{memory["usage_percent"]:.0f}% used'
        )
        self.value_labels["storage"].configure(
            text=f"{total_storage:.1f} GB"
        )
        self.value_labels["uptime"].configure(
            text=system["uptime"]
        )

    def update_cpu(self, cpu):
        self.clear_frame(self.cpu_frame)

        self.add_info_row(
            self.cpu_frame, "Processor", cpu["processor"]
        )
        self.add_info_row(
            self.cpu_frame, "Architecture", cpu["architecture"]
        )
        self.add_info_row(
            self.cpu_frame, "Physical Cores", cpu["physical_cores"]
        )
        self.add_info_row(
            self.cpu_frame, "Logical Cores", cpu["logical_cores"]
        )
        self.add_info_row(
            self.cpu_frame, "Current Speed", cpu["current_speed"]
        )
        self.add_info_row(
            self.cpu_frame, "Maximum Speed", cpu["max_speed"]
        )
        self.add_info_row(
            self.cpu_frame, "Current Usage",
            f'{cpu["usage_percent"]:.1f}%'
        )

    def update_memory(self, memory):
        self.clear_frame(self.memory_frame)

        self.add_info_row(
            self.memory_frame, "Total RAM",
            f'{memory["total_gb"]} GB'
        )
        self.add_info_row(
            self.memory_frame, "Used RAM",
            f'{memory["used_gb"]} GB'
        )
        self.add_info_row(
            self.memory_frame, "Available RAM",
            f'{memory["available_gb"]} GB'
        )
        self.add_info_row(
            self.memory_frame, "RAM Usage",
            f'{memory["usage_percent"]:.1f}%'
        )
        self.add_info_row(
            self.memory_frame, "Swap Usage",
            f'{memory["swap_used_gb"]} / '
            f'{memory["swap_total_gb"]} GB '
            f'({memory["swap_percent"]:.1f}%)'
        )

    def update_disks(self, disks):
        self.clear_frame(self.disk_frame)

        if not disks:
            self.add_info_row(
                self.disk_frame, "Storage",
                "No accessible drives found."
            )
            return

        table = self.create_table(
            self.disk_frame,
            ("device", "filesystem", "total", "used", "free", "usage"),
            ("Drive", "File System", "Total GB",
             "Used GB", "Free GB", "Usage")
        )

        for disk in disks:
            table.insert(
                "",
                "end",
                values=(
                    disk["device"],
                    disk["filesystem"],
                    disk["total_gb"],
                    disk["used_gb"],
                    disk["free_gb"],
                    f'{disk["usage_percent"]:.1f}%'
                )
            )

    def update_network(self, adapters):
        self.clear_frame(self.network_frame)

        if not adapters:
            self.add_info_row(
                self.network_frame, "Network",
                "No network adapters found."
            )
            return

        table = self.create_table(
            self.network_frame,
            ("name", "status", "speed", "ipv4", "sent", "received"),
            ("Adapter", "Status", "Speed Mbps",
             "IPv4 Address", "Sent MB", "Received MB")
        )

        for adapter in adapters:
            table.insert(
                "",
                "end",
                values=(
                    adapter["name"],
                    adapter["status"],
                    adapter["speed_mbps"] or "Unknown",
                    adapter["ipv4"],
                    adapter["bytes_sent_mb"],
                    adapter["bytes_received_mb"]
                )
            )

    def update_extra(self, battery, temperature):
        self.clear_frame(self.extra_frame)

        if battery["available"]:
            self.add_info_row(
                self.extra_frame, "Battery",
                f'{battery["percent"]:.0f}%'
            )
            self.add_info_row(
                self.extra_frame, "Power",
                battery["power_status"]
            )
            self.add_info_row(
                self.extra_frame, "Time Remaining",
                battery["time_remaining"]
            )
        else:
            self.add_info_row(
                self.extra_frame, "Battery",
                battery["message"]
            )

        if temperature["available"]:
            for reading in temperature["readings"]:
                current = reading["current_celsius"]

                self.add_info_row(
                    self.extra_frame,
                    f'{reading["sensor"]} - {reading["label"]}',
                    f"{current} °C"
                    if current is not None
                    else "Not available"
                )
        else:
            self.add_info_row(
                self.extra_frame,
                "Temperature",
                temperature["message"]
            )

    def update_system(self, system):
        self.clear_frame(self.system_frame)

        rows = [
            ("Computer Name", system["computer_name"]),
            ("Operating System", system["operating_system"]),
            ("OS Release", system["os_release"]),
            ("OS Version", system["os_version"]),
            ("System Architecture", system["architecture"]),
            ("Python Version", system["python_version"]),
            ("Last Boot Time", system["boot_time"]),
            ("System Uptime", system["uptime"]),
        ]

        for label, value in rows:
            self.add_info_row(self.system_frame, label, value)
