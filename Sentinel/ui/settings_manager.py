import json
from pathlib import Path


class SettingsManager:
    def __init__(self):
        self.settings_file = (
            Path(__file__).resolve().parent.parent / "settings.json"
        )

        self.default_settings = {
            "cpu_limit": 85,
            "ram_limit": 85,
            "disk_limit": 90,
            "dashboard_refresh_seconds": 2,
            "process_refresh_seconds": 5
        }

        self.settings = self.default_settings.copy()
        self.load_settings()

    def load_settings(self):
        """Load saved settings or create defaults when necessary."""
        if not self.settings_file.exists():
            self.save_settings()
            return self.get_settings()

        try:
            with open(self.settings_file, "r", encoding="utf-8") as file:
                saved_settings = json.load(file)

            if not isinstance(saved_settings, dict):
                raise ValueError("Settings file must contain a JSON object.")

            updated_settings = self.default_settings.copy()

            for key in self.default_settings:
                if key in saved_settings:
                    updated_settings[key] = saved_settings[key]

            self.settings = self._validate_settings(updated_settings)

        except (OSError, json.JSONDecodeError, ValueError, TypeError):
            self.settings = self.default_settings.copy()
            self.save_settings()

        return self.get_settings()

    def save_settings(self):
        """Save the current settings to the JSON configuration file."""
        try:
            self.settings = self._validate_settings(self.settings)

            with open(
                self.settings_file,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    self.settings,
                    file,
                    indent=4
                )

            return True

        except (OSError, ValueError, TypeError) as error:
            print(f"Unable to save Sentinel settings: {error}")
            return False

    def get_settings(self):
        """Return a copy of all current settings."""
        return self.settings.copy()

    def get_setting(self, key):
        """Return one setting, or None if the key does not exist."""
        return self.settings.get(key)

    def update_settings(self, new_settings):
        """Validate and save supplied setting changes."""
        if not isinstance(new_settings, dict):
            return False

        updated_settings = self.settings.copy()

        for key, value in new_settings.items():
            if key not in self.default_settings:
                continue

            updated_settings[key] = value

        try:
            updated_settings = self._validate_settings(
                updated_settings
            )
        except (ValueError, TypeError):
            return False

        previous_settings = self.settings.copy()
        self.settings = updated_settings

        if not self.save_settings():
            self.settings = previous_settings
            return False

        return True

    def reset_settings(self):
        """Restore and save the default settings."""
        previous_settings = self.settings.copy()
        self.settings = self.default_settings.copy()

        if not self.save_settings():
            self.settings = previous_settings
            return False

        return True

    def _validate_settings(self, settings):
        """Check that thresholds and refresh intervals are valid."""
        validated = self.default_settings.copy()

        for key in validated:
            value = settings.get(key, validated[key])

            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{key} must be a number.")

            if not float(value).is_integer():
                raise ValueError(f"{key} must be a whole number.")

            value = int(value)

            if key in ("cpu_limit", "ram_limit", "disk_limit"):
                if not 1 <= value <= 100:
                    raise ValueError(
                        f"{key} must be between 1 and 100."
                    )

            elif key == "dashboard_refresh_seconds":
                if not 1 <= value <= 60:
                    raise ValueError(
                        "Dashboard refresh must be between 1 and 60 seconds."
                    )

            elif key == "process_refresh_seconds":
                if not 2 <= value <= 300:
                    raise ValueError(
                        "Process refresh must be between 2 and 300 seconds."
                    )

            validated[key] = value

        return validated
