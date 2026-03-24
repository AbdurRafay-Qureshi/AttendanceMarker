import os
import shutil
import tempfile
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

import config
from app import create_app
from database.db import db
from database.models import AudioRecording, MeetingSession, Settings


class _FakeMeetingBot:
    def __init__(self, session_id, meeting_link, provider, socketio):
        self.session_id = session_id
        self.meeting_link = meeting_link
        self.provider = provider
        self.socketio = socketio

    def run(self):
        return None


class _ImmediateThread:
    def __init__(self, target=None, daemon=None):
        self._target = target
        self.daemon = daemon

    def start(self):
        if self._target:
            self._target()


class MeetingRouteIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.old_db_uri = config.SQLALCHEMY_DATABASE_URI
        self.db_fd, self.db_path = tempfile.mkstemp(prefix='meetbot-test-', suffix='.db')
        config.SQLALCHEMY_DATABASE_URI = f'sqlite:///{self.db_path}'
        self.app = create_app()
        self.client = self.app.test_client()

        self.profile_root = tempfile.mkdtemp(prefix='profile-root-')
        self.managed_root = tempfile.mkdtemp(prefix='managed-root-')
        os.makedirs(os.path.join(self.profile_root, 'Default'), exist_ok=True)

        with self.app.app_context():
            settings = Settings.get()
            settings.display_name = 'Test User'
            settings.chrome_profile_path = self.profile_root
            settings.chrome_profile_name = 'Default'
            settings.profile_mode = 'linked_profile'
            db.session.add(AudioRecording(file_path='dummy.wav'))
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
        shutil.rmtree(self.profile_root, ignore_errors=True)
        shutil.rmtree(self.managed_root, ignore_errors=True)

    @patch('routes.meeting.threading.Thread', _ImmediateThread)
    @patch('services.meeting_bot.MeetingBot', _FakeMeetingBot)
    def test_start_route_creates_teams_session(self):
        response = self.client.post(
            '/meeting/start',
            data={
                'provider': 'teams',
                'meeting_link': 'https://teams.microsoft.com/l/meetup-join/19%3ameeting_x%40thread.v2/0?context=%7b%7d',
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload['success'])
        self.assertEqual(payload['provider'], 'teams')

        with self.app.app_context():
            session = db.session.get(MeetingSession, payload['session_id'])
            self.assertIsNotNone(session)
            self.assertEqual(session.provider, 'teams')




if __name__ == '__main__':
    unittest.main()
