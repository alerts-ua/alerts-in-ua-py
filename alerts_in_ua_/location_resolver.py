from typing_extensions import Dict, Union, Optional


class LocationUidResolver:
    UID_TO_LOCATION: Dict[int, str] = {
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
    LOCATION_TO_UID: Dict[str, Union[int, str]] = dict(
        zip(UID_TO_LOCATION.values(), UID_TO_LOCATION.keys())
    )

    @classmethod
    def resolve_uid(cls, title: str):
        """Resolve location to UID."""
        return cls.LOCATION_TO_UID.get(str(title), f"Unknown UID for {title=}")

    @classmethod
    def resolve_title(cls, uid: int):
        """Resolve UID to location."""
        return cls.UID_TO_LOCATION.get(int(uid), f"Unknown location for uid {uid=}")


__all__ = ('LocationUidResolver',)
