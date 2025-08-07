from typing import List, Optional
from .air_raid_alert_status import AirRaidAlertStatus

class AirRaidAlertStatuses:
    """
    Container class for AirRaidAlertStatus objects.
    Provides filtering and iteration capabilities.
    """
    
    def __init__(self, statuses: List[AirRaidAlertStatus]):
        """
        Initialize AirRaidAlertStatuses with a list of status objects.
        
        Args:
            statuses (List[AirRaidAlertStatus]): List of air raid alert status objects
        """
        self.statuses = statuses
        # Create a cache mapping UID to status for fast lookups
        self._uid_cache = {}
        for status in statuses:
            # Extract UID from location_title if possible, or use location_title as key
            # This assumes the status objects have been created with proper UID mapping    
            self._uid_cache[status.uid] = status
        
    
    def filter_by_status(self, status: str) -> List[AirRaidAlertStatus]:
        """
        Filter statuses by a specific status value.
        
        Args:
            status (str): Status to filter by ('no_alert', 'active', 'partly')
            
        Returns:
            List[AirRaidAlertStatus]: Filtered list of status objects
        """
        return [status_obj for status_obj in self.statuses if status_obj.status == status]
    
    def get_active_alert_statuses(self) -> List[AirRaidAlertStatus]:
        """
        Get all statuses with active alerts.
        
        Returns:
            List[AirRaidAlertStatus]: List of status objects with active alerts
        """
        return self.filter_by_status('active')
    
    def get_partly_active_alert_statuses(self) -> List[AirRaidAlertStatus]:
        """
        Get all statuses with partial alerts.
        
        Returns:
            List[AirRaidAlertStatus]: List of status objects with partial alerts
        """
        return self.filter_by_status('partly')
    
    def get_no_alert_statuses(self) -> List[AirRaidAlertStatus]:
        """
        Get all statuses with no alerts.
        
        Returns:
            List[AirRaidAlertStatus]: List of status objects with no alerts
        """
        return self.filter_by_status('no_alert')
    
    def get_status(self, uid) -> Optional[AirRaidAlertStatus]:
        """
        Get status by UID using cached lookup.
        
        Args:
            uid: The UID to look up (can be int or location title string)
            
        Returns:
            Optional[AirRaidAlertStatus]: The status object if found, None otherwise
        """
        return self._uid_cache.get(uid)
    
    def __iter__(self):
        """Make the container iterable."""
        return iter(self.statuses)
    
    def __len__(self) -> int:
        """Return the number of status objects."""
        return len(self.statuses)
    
    def __getitem__(self, index):
        """Allow indexing into the statuses list."""
        return self.get_status(index)
    
    def __repr__(self) -> str:
        return f"AirRaidAlertStatuses({self.statuses})"
    
    def __str__(self) -> str:
        return f"AirRaidAlertStatuses with {len(self.statuses)} statuses"
