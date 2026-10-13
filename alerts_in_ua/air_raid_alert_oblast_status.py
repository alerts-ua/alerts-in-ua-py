class AirRaidAlertOblastStatus:
    STATUS_MAP = {'A': 'active', 'R': 'active', 'Y': 'active', 'P': 'partly', 'N': 'no_alert'}
    LEVEL_MAP = {'R': 'red', 'Y': 'yellow'}
    def __init__(self, location_title: str, status: str, oblast_level_only: bool = False):
        self.alert_level = self.LEVEL_MAP.get(status)
        status = self.STATUS_MAP.get(status, 'no_alert')
        if status == 'partly' and oblast_level_only:
            status = 'no_alert'
        self.status = status
        self.location_title = location_title

    def is_active_on_all_oblast(self) -> bool:
        return self.status == "active"

    def is_partly_active(self) -> bool:
        return self.status == "partly"

    def is_no_alert(self) -> bool:
        return self.status == "no_alert"

    def is_red(self) -> bool:
        return self.alert_level == "red"

    def is_yellow(self) -> bool:
        return self.alert_level == "yellow"

    def location_title(self) -> str:
        return self.location_title

    def __repr__(self) -> str:
        if self.status == "active" and self.alert_level == "yellow":
            return f"🟠 {self.location_title}"
        elif self.status == "active":
            return f"🔴 {self.location_title}"
        elif self.status == "partly":
            return f"🟡 {self.location_title}"
        else:
            return f"🟢 {self.location_title}"

    def __str__(self) -> str:
        return f"{self.status}:{self.location_title}"