import unittest

from services.provider_routing import (
    detect_provider_from_link,
    resolve_provider,
    validate_link_for_provider,
)


class ProviderRoutingTests(unittest.TestCase):
    def test_detect_provider_from_link(self):
        self.assertEqual(detect_provider_from_link('https://meet.google.com/abc-defg-hij'), 'meet')
        self.assertEqual(
            detect_provider_from_link('https://teams.microsoft.com/l/meetup-join/19%3ameeting_x%40thread.v2/0'),
            'teams',
        )
        self.assertEqual(
            detect_provider_from_link('https://teams.live.com/meetup-join/123'),
            'teams',
        )
        self.assertIsNone(detect_provider_from_link('https://example.com/meeting'))

    def test_resolve_provider_prefers_explicit_override(self):
        link = 'https://meet.google.com/abc-defg-hij'
        self.assertEqual(resolve_provider(link, 'teams'), 'teams')
        self.assertEqual(resolve_provider(link, ''), 'meet')

    def test_validate_meet_links(self):
        self.assertTrue(validate_link_for_provider('https://meet.google.com/abc-defg-hij', 'meet'))
        self.assertFalse(validate_link_for_provider('https://meet.google.com/', 'meet'))
        self.assertFalse(validate_link_for_provider('https://example.com/abc-defg-hij', 'meet'))

    def test_validate_teams_links(self):
        self.assertTrue(
            validate_link_for_provider(
                'https://teams.microsoft.com/l/meetup-join/19%3ameeting_x%40thread.v2/0?context=%7b%7d',
                'teams',
            )
        )
        self.assertFalse(validate_link_for_provider('https://teams.microsoft.com/', 'teams'))
        self.assertFalse(validate_link_for_provider('https://meet.google.com/abc-defg-hij', 'teams'))


if __name__ == '__main__':
    unittest.main()
