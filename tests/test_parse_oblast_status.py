from unittest import TestCase

from alerts_in_ua_.alerts import AirRaidOblastStatuses


class TestParseOblastStatus(TestCase):

    def test_parse_oblast_status(self):
        obj_ = AirRaidOblastStatuses('A' * 3 + 'N' * 20 + 'P' * 3 + '_')
        print(obj_)
        print(repr(obj_))

        print(obj_[0])
        print(repr(obj_[0]))
