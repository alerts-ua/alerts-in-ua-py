import os
from unittest import TestCase

from alerts_in_ua import Client
from alerts_in_ua_.alert import LocationType
from alerts_in_ua_.alerts import Alerts, FilterCriterion


class TestFetch(TestCase):
    class TestClient(Client):

        def get_active_alerts(self, use_cache=True) -> Alerts:
            """Custom fetch definition"""
            data = self._request("alerts/active.json", use_cache=use_cache)
            return Alerts(**data)

    def setUp(self) -> None:
        self.token = os.environ["API_TOKEN"]
        self.client = self.TestClient(token=self.token)
        self.alerts_details = self.client.get_active_alerts(False)
        # self.alerts_states = self.client.get_air_raid_alert_statuses_by_oblast(True)

    def test_fetch_result(self):
        self.assertIsNotNone(self.alerts_details[0].id)

    def test_filter(self):
        filtered = self.alerts_details.filter(
            FilterCriterion('location_uid', 16),
            ('location_type', LocationType.OBLAST),
            ('location_type', 'oblast')
        )
        self.assertIsInstance(filtered, list)

    # def test_fetch_short_states_result(self):
    #     print(self.alerts_states)
