import asyncio
from unittest import TestCase

from alerts_in_ua import Client
from alerts_in_ua.alert import LocationType, AlertDetails
from alerts_in_ua.alerts import Alerts, FilterCriterion, AirRaidOblastStatuses, AirRaidOblastStatus, HistoryPeriod


class TestFetch(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def validete_alerts(self, alerts):
        self.assertIsInstance(alerts, Alerts)
        self.assertIsNotNone(alerts[0], AlertDetails)
        self.assertIsNotNone(alerts[0].id)

    def test_fetch_result(self):

        with self.subTest("Test sync"):
            alerts = self.client.get_active(False)
            self.validete_alerts(alerts)

        with self.subTest("Test async"):
            alerts = asyncio.run(self.client.async_get_active(False))
            self.validete_alerts(alerts)

        with self.subTest("Test alerts filter"):
            filtered = alerts.filter(
                FilterCriterion('location_uid', 16),
                ('location_type', LocationType.OBLAST),
                ('location_type', 'oblast')
            )
            self.assertIsInstance(filtered, list)

    def test_fetch_history(self):

        with self.subTest("Test sync"):
            alerts = self.client.get_history(16, HistoryPeriod.DAY_AGO)
            self.validete_alerts(alerts)

        with self.subTest("Test async"):
            alerts = asyncio.run(self.client.async_get_history(16, HistoryPeriod.DAY_AGO))
            self.validete_alerts(alerts)

    def test_oblast_statuses(self):
        with self.subTest("Test sync single"):
            statuses = self.client.get_air_raid(16, False)
            self.assertIsInstance(statuses, AirRaidOblastStatus)

        with self.subTest("Test async single"):
            statuses = asyncio.run(self.client.async_get_air_raid(16, False))
            self.assertIsInstance(statuses, AirRaidOblastStatus)

        with self.subTest("Test sync all"):
            statuses = self.client.get_air_raids(False)
            self.assertIsInstance(statuses, AirRaidOblastStatuses)

        with self.subTest("Test async all"):
            statuses = asyncio.run(self.client.async_get_air_raids(False))
            self.assertIsInstance(statuses, AirRaidOblastStatuses)
