import warnings
import unittest
import os
from badpackets.session import BadPacketsSession


class TestStringMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_url = os.getenv("BADPACKETS_API_URL")
        cls.api_key = os.getenv("BADPACKETS_API_TOKEN")
        cls.session = BadPacketsSession(cls.api_url, cls.api_key)

    def setUp(self):
        warnings.filterwarnings(
            "ignore",
            category=ResourceWarning,
            message="unclosed.*<ssl.SSLSocket.*>"
        )

    def test_bad_api_key(self):
        bad_key_session = BadPacketsSession(self.api_url, "some_bad_key")
        response = bad_key_session.get('ping')
        self.assertEqual(response.status_code, 403)

    def test_working_api_key(self):
        response = self.session.get('ping')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
