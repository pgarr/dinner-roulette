import json
import unittest

from app import create_app, db
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class TestAppSetUp(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_connection(self):
        with self.app.test_client() as c:
            r = c.get('/api/')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(json.loads(r.get_data()), {'message': 'API is online!'})
