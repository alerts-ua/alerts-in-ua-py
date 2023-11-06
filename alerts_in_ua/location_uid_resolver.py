class LocationUidResolver:
    def __init__(self):
        self.uid_to_location = {
            3: "Хмельницька область",
            4: "Вінницька область",
            5: "Рівненська область",
            8: "Волинська область",
            9: "Дніпропетровська область",
            10: "Житомирська область",
            11: "Закарпатська область",
            12: "Запорізька область",
            13: "Івано-Франківська область",
            14: "Київська область",
            15: "Кіровоградська область",
            16: "Луганська область",
            17: "Миколаївська область",
            18: "Одеська область",
            19: "Полтавська область",
            20: "Сумська область",
            21: "Тернопільська область",
            22: "Харківська область",
            23: "Херсонська область",
            24: "Черкаська область",
            25: "Чернігівська область",
            26: "Чернівецька область",
            27: "Львівська область",
            28: "Донецька область",
            29: "Автономна Республіка Крим",
            30: "м. Севастополь",
            31: "м. Київ"
        }
        # Inverse mapping from location to UID
        self.location_to_uid = {v: k for k, v in self.uid_to_location.items()}

    def resolve_uid(self, uid):
        """Resolve location to UID."""
        return self.location_to_uid.get(uid, "Unknown UID")

    def resolve_location_title(self, uid):
        """Resolve UID to location."""
        return self.uid_to_location.get(int(uid), "Unknown location")