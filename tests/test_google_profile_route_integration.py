import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

import config
from app import create_app
from database.db import db
from database.models import Settings


class _NoOpThread:
    def __init__(self, target=None, daemon=None):
        self._target = target
        self.daemon = daemon

    def start(self):
        return None


class GoogleProfileRouteIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.old_db_uri = config.SQLALCHEMY_DATABASE_URI
        self.db_fd, self.db_path = tempfile.mkstemp(prefix='meetbot-test-', suffix='.db')
        config.SQLALCHEMY_DATABASE_URI = f'sqlite:///{self.db_path}'
        self.app = create_app()
        self.client = self.app.test_client()
        self.managed_root = tempfile.mkdtemp(prefix='managed-parent-')
        self.managed_dir = os.path.join(self.managed_root, 'meetbot-session')

        with self.app.app_context():
            settings = Settings.get()
            settings.display_name = 'Test User'
            db.session.commit()

    def tearDown(self):
        config.SQLALCHEMY_DATABASE_URI = self.old_db_uri
        with self.app.app_context():
            db.session.remove()
            db.engine.dispose()
        try:
            os.close(self.db_fd)
        except Exception:
            pass
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
        if os.path.isdir(self.managed_root):
            shutil.rmtree(self.managed_root, ignore_errors=True)

    @patch('routes.google_profile.threading.Thread', _NoOpThread)
    def test_launch_login_persists_managed_folder_mode(self):
        from routes import google_profile

        google_profile._login_browser_open = False
        response = self.client.post(
            '/google/launch-login',
            json={
                'profile_mode': 'managed_folder',
                'browser_type': 'edge',
                'managed_user_data_dir': self.managed_dir,
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload['success'])

        with self.app.app_context():
            settings = Settings.get()
            self.assertEqual(settings.profile_mode, 'managed_folder')
            self.assertEqual(settings.browser_type, 'edge')
            self.assertEqual(settings.managed_user_data_dir, os.path.abspath(self.managed_dir))
            self.assertTrue(os.path.isdir(settings.managed_user_data_dir))

    @patch('routes.google_profile.threading.Thread', _NoOpThread)
    def test_launch_login_rejects_managed_folder_for_chrome(self):
        from routes import google_profile

        google_profile._login_browser_open = False
        response = self.client.post(
            '/google/launch-login',
            json={
                'profile_mode': 'managed_folder',
                'browser_type': 'chrome',
                'managed_user_data_dir': self.managed_dir,
            },
        )

        self.assertEqual(response.status_code, 400)
        payload = response.get_json()
        self.assertIn('Edge only', payload.get('error', ''))


if __name__ == '__main__':
    unittest.main()
