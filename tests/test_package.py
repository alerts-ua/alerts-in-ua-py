import unittest

import alerts_in_ua


class PackageTestCase(unittest.TestCase):

    def test_public_exports(self):
        for name in ["Client", "AsyncClient", "Threat", "ApiError", "UnauthorizedError",
                     "ForbiddenError", "RateLimitError", "InternalServerError"]:
            self.assertTrue(hasattr(alerts_in_ua, name), name)
        self.assertTrue(issubclass(alerts_in_ua.RateLimitError, alerts_in_ua.ApiError))


if __name__ == "__main__":
    unittest.main()
