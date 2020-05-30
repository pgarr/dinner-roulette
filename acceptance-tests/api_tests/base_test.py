import os
from unittest import TestCase

from dotenv import load_dotenv

from utils.aut import Aut


class BaseTest(TestCase):

    def setUp_users(self):
        return [{"username": "test", "email": "test@test.com", "password": "test"},
                {"username": "test2", "email": "test2@test.com", "password": "test"},
                {"username": "admin", "email": "admin@test.com", "password": "admin"}]

    def setUp_recipes(self):
        return None

    def setUp_waiting_recipes(self):
        return None

    @classmethod
    def setUpClass(cls):
        basedir = os.path.abspath(os.path.dirname(__file__))
        load_dotenv(os.path.join(basedir, '..', '.env'))

    def setUp(self):
        # run aut
        self._aut = Aut(users=self.setUp_users(), recipes=self.setUp_recipes(),
                        waiting_recipes=self.setUp_waiting_recipes())
        self._aut.run(10)

    def tearDown(self):
        self._aut.stop()
