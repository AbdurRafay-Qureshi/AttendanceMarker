import unittest

from services.teams_utils import contains_detection_term, is_auth_redirect_url, is_waiting_lobby_text


class TeamsUtilsTests(unittest.TestCase):
    def test_auth_redirect_detection(self):
        self.assertTrue(is_auth_redirect_url('https://login.microsoftonline.com/common/oauth2/v2.0/authorize'))
        self.assertTrue(is_auth_redirect_url('https://login.live.com/login.srf'))
        self.assertFalse(is_auth_redirect_url('https://teams.microsoft.com/l/meetup-join/abc'))

    def test_contains_detection_term(self):
        matched, term, normalized = contains_detection_term('Burhan Khatri, please mark attendance', ['burhan', '2024123'])
        self.assertTrue(matched)
        self.assertEqual(term, 'burhan')
        self.assertIn('burhan', normalized)

        matched, term, _ = contains_detection_term('hello class', ['roll 22'])
        self.assertFalse(matched)
        self.assertIsNone(term)

    def test_waiting_lobby_detection(self):
        self.assertTrue(is_waiting_lobby_text('You are in the lobby. Someone in the meeting should let you in soon.'))
        self.assertFalse(is_waiting_lobby_text('Meeting is live and connected.'))


if __name__ == '__main__':
    unittest.main()
