class AirRaidAlertOblastStatus:
    def __init__(self, location_title: str, status: str):
        if status not in ['partly', 'active', 'no_alert']:
           raise ValueError("Invalid status")
        self.status = status
        self.location_title = location_title

    def is_active_on_all_oblast(self) -> bool:
        return self.status == "active"

    def is_partly_active(self) -> bool:
        return self.status == "partly"

    def is_no_alert(self) -> bool:
        return self.status == "no_alert"

    def location_title(self) -> str:
        return self.location_title

    def __repr__(self) -> str:
        if self.status == "active":
            return f"🔴 {self.location_title}"
        elif self.status == "partly":
            return f"🟡 {self.location_title}"
        else:
            return f"🟢 {self.location_title}"

    def __str__(self) -> str:
        return f"{self.status}{self.location_title}"