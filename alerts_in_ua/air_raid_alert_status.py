class AirRaidAlertStatus:
    """
    Represents air raid alert status for a specific location.
    This class is used for the get_air_raid_alert_statuses method.
    """
    
    def __init__(self, location_title: str, status: str, uid: int = None):
        """
        Initialize AirRaidAlertStatus.
        
        Args:
            location_title (str): The title/name of the location
            status (str): The alert status ('no_alert', 'active', 'partly')
            uid (int, optional): The UID of the location
        """
        self.location_title = location_title
        self.status = status
        self.uid = uid
    
    def __repr__(self) -> str:
        if self.status == "active":
            return f"🔴 {self.location_title}"
        elif self.status == "partly":
            return f"🟡 {self.location_title}"
        else:
            return f"🟢 {self.location_title}"

    def __str__(self) -> str:
        return f"{self.status}:{self.location_title}"
