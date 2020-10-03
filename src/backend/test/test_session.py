import unittest
from badpackets.session import BadPacketsSession

class TestStringMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_url = "https://api.badpackets.net/v1/"
        cls.api_key = "enter_api_key"
        cls.bp_auth_session = BadPacketsSession(cls.api_url, cls.api_key)
        cls.bp_unauth_session = BadPacketsSession(cls.api_url)

    def test_ping(self):
        response = self.bp_unauth_session.get('/ping')
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated(self):
        response = self.bp_unauth_session.get('/query?tags=Mirai')
        self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()