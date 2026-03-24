import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from routes import google_profile


class GoogleProfileUtilsTests(unittest.TestCase):
    def test_browser_type_from_prog_id(self):
        self.assertEqual(google_profile._browser_type_from_prog_id('MSEdgeHTM'), 'edge')
        self.assertEqual(google_profile._browser_type_from_prog_id('ChromeHTML'), 'chrome')
        self.assertEqual(google_profile._browser_type_from_prog_id('ChromiumHTM'), 'chrome')
        self.assertIsNone(google_profile._browser_type_from_prog_id('FirefoxURL'))

    def test_profile_is_valid_respects_browser_roots(self):
        root_edge = tempfile.mkdtemp(prefix='edge-root-')
        root_chrome = tempfile.mkdtemp(prefix='chrome-root-')
        try:
            edge_profile = 'Default'
            chrome_profile = 'Profile 1'
            os.makedirs(os.path.join(root_edge, edge_profile), exist_ok=True)
            os.makedirs(os.path.join(root_chrome, chrome_profile), exist_ok=True)

            with patch.object(
                google_profile,
                '_detect_browser_roots',
                return_value={'edge': [root_edge], 'chrome': [root_chrome]},
            ):
                self.assertTrue(google_profile._profile_is_valid(root_edge, edge_profile, 'edge'))
                self.assertTrue(google_profile._profile_is_valid(root_chrome, chrome_profile, 'chrome'))
                self.assertFalse(google_profile._profile_is_valid(root_edge, edge_profile, 'chrome'))
                self.assertFalse(google_profile._profile_is_valid(root_chrome, chrome_profile, 'edge'))
        finally:
            shutil.rmtree(root_edge, ignore_errors=True)
            shutil.rmtree(root_chrome, ignore_errors=True)

    def test_normalize_profile_mode(self):
        self.assertEqual(google_profile._normalize_profile_mode('managed_folder'), 'managed_folder')
        self.assertEqual(google_profile._normalize_profile_mode('linked_profile'), 'linked_profile')
        self.assertEqual(google_profile._normalize_profile_mode('invalid-mode'), 'linked_profile')

    def test_validate_managed_user_data_dir(self):
        parent = tempfile.mkdtemp(prefix='managed-root-')
        try:
            target = os.path.join(parent, 'session-data')
            normalized, error = google_profile._validate_managed_user_data_dir('edge', target)
            self.assertIsNone(error)
            self.assertEqual(normalized, os.path.abspath(target))
            self.assertTrue(os.path.isdir(normalized))

            normalized, error = google_profile._validate_managed_user_data_dir('chrome', target)
            self.assertIsNone(normalized)
            self.assertIn('Edge only', error)
        finally:
            shutil.rmtree(parent, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
