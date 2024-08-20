from unittest import TestCase
from alerts_in_ua import Client
from alerts_in_ua_.alerts import Alerts

class TestFetch(TestCase):

    def test_fetch(self):

        class C(Client):

            def get_active_alerts(self, use_cache=True) -> Alerts:
                data = self._request("alerts/active.json", use_cache=use_cache)
                return Alerts(**data)

        c = C(token='')
        a = c.get_active_alerts(False)
        print(type(a.alerts[0]))
