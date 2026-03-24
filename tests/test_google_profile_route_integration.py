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
            settings.chrome_profile_path = self.managed_root
            settings.chrome_profile_name = 'Default'
            os.makedirs(os.path.join(self.managed_root, 'Default'), exist_ok=True)
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




if __name__ == '__main__':
    unittest.main()
