class AirRaidAlertStatusResolver:
    """
    Resolves air raid alert status characters from the API to meaningful status values.
    
    The API returns a string where each character represents the status of a region by its UID index:
    - N: No alert (Немає тривоги)
    - A: Active alert (Активна тривога), v1 only
    - R: Active alert, red level (Активна тривога, червоний рівень), v2 only
    - Y: Active alert, yellow level (Активна тривога, жовтий рівень), v2 only
    - P: Partial alert (Часткова тривога)
    - (space): No data for region (UID not assigned to any region)
    """
    
    STATUS_MAPPING = {
        'N': 'no_alert',    # Немає тривоги
        'A': 'active',      # Активна тривога
        'R': 'active',      # Активна тривога, червоний рівень
        'Y': 'active',      # Активна тривога, жовтий рівень
        'P': 'partly',      # Часткова тривога
        ' ': 'undefined',    # Немає даних для регіону 
    }

    LEVEL_MAPPING = {
        'R': 'red',
        'Y': 'yellow',
    }
    
    @classmethod
    def resolve_status_char(cls, status_char: str) -> str:
        """
        Resolves a single status character to its corresponding status value.
        
        Args:
            status_char (str): The character from the API response
            
        Returns:
            str: The resolved status value ('no_alert', 'active', or 'partly')
        """
        return cls.STATUS_MAPPING.get(status_char, 'no_alert')

    @classmethod
    def resolve_level_char(cls, status_char: str):
        """
        Resolves a single status character to its alert level.

        Args:
            status_char (str): The character from the API response

        Returns:
            Optional[str]: 'red' or 'yellow' for v2 active statuses, None otherwise
        """
        return cls.LEVEL_MAPPING.get(status_char)
    
    @classmethod
    def resolve_status_string(cls, status_string: str, uid_to_location_mapping: dict) -> list:
        """
        Resolves a complete status string to a list of status dictionaries.
        Filters out statuses with 'undefined' status.
        
        Args:
            status_string (str): The complete status string from the API
            uid_to_location_mapping (dict): Mapping of UID to location title
            
        Returns:
            list: List of dictionaries with 'uid', 'location_title', 'status' and 'alert_level' keys
        """
        resolved_statuses = []
        
        for uid in range(len(status_string)):
            status_char = status_string[uid]
            status = cls.resolve_status_char(status_char)
            
            # Skip statuses with 'undefined' status
            if status != 'undefined':
                # Get location title from mapping, or use fallback
                location_title = uid_to_location_mapping.get(uid, f"Локація #{uid}")
                
                resolved_statuses.append({
                    'uid': uid,
                    'location_title': location_title,
                    'status': status,
                    'alert_level': cls.resolve_level_char(status_char)
                })
       
                
        return resolved_statuses
