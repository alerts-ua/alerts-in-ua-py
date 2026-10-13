import copy
import json
import pathlib

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


def load_fixture(name: str = "active_alerts.json") -> dict:
    with open(FIXTURES / name, encoding="utf-8") as f:
        return json.load(f)


def alert_by_id(data: dict, alert_id: int) -> dict:
    return copy.deepcopy(next(a for a in data["alerts"] if a["id"] == alert_id))
