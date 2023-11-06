from typing import List
from .air_raid_alert_oblast_status import AirRaidAlertOblastStatus
class AirRaidAlertOblastStatuses:
     LOCATIONS = [
            "Автономна Республіка Крим",
            "Волинська область",
            "Вінницька область",
            "Дніпропетровська область",
            "Донецька область",
            "Житомирська область",
            "Закарпатська область",
            "Запорізька область",
            "Івано-Франківська область",
            "м. Київ",
            "Київська область",
            "Кіровоградська область",
            "Луганська область",
            "Львівська область",
            "Миколаївська область",
            "Одеська область",
            "Полтавська область",
            "Рівненська область",
            "м. Севастополь",
            "Сумська область",
            "Тернопільська область",
            "Харківська область",
            "Херсонська область",
            "Хмельницька область",
            "Черкаська область",
            "Чернівецька область",
            "Чернігівська область"
        ]


     def __init__(self, data: str, oblast_level_only: bool = False):
        self.oblast_statuses = []
        for i, location in enumerate(self.LOCATIONS):
            status = data[i]
            self.oblast_statuses.append(AirRaidAlertOblastStatus(location, status,oblast_level_only=oblast_level_only))

     def filter_by_status(self, status):
        return [oblast_status for oblast_status in self.oblast_statuses if oblast_status.status == status]

     def get_active_alert_oblasts(self) -> List[AirRaidAlertOblastStatus]:
        return self.filter_by_status('active')

     def get_partly_active_alert_oblasts(self) -> List[AirRaidAlertOblastStatus]:
        return self.filter_by_status('partly')

     def get_no_alert_oblasts(self) -> List[AirRaidAlertOblastStatus]:
        return self.filter_by_status('no_alert')

     def __iter__(self) -> List[AirRaidAlertOblastStatus]:
        return iter(self.oblast_statuses)

     def __repr__(self) -> str:
         return str(self.oblast_statuses)