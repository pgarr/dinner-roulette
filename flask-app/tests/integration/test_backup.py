import re

from app import db
from app.backup import dump_backup
from app.models import User
from tests.base_test import TestAppSetUp


class TestBackup(TestAppSetUp):
    def setUp(self):
        super().setUp()

        # users test test2 admin
        user = User(username="test", email="test@test.com")
        user.set_password("test")
        db.session.add(user)
        user2 = User(username="test2", email="test2@test.com")
        user2.set_password("test")
        db.session.add(user2)
        admin = User(username="admin", email="admin@test.com")
        admin.set_password("admin")
        db.session.add(admin)

        db.session.commit()

        self.user_pattern = '{\"user\": \[{\"id\": 1, \"username\": \"test\", \"email\": \"test@test\.com\", \"password_hash\":' \
                            ' \"pbkdf2:sha256:150000\$.*\"}, {\"id\": 2, \"username\": \"test2\", \"email\": \"test2@test\.com\",' \
                            ' \"password_hash\": \"pbkdf2:sha256:150000\$.*\"}, {\"id\": 3, \"username\": \"admin\", \"email\":' \
                            ' \"admin@test\.com\", \"password_hash\": \"pbkdf2:sha256:150000\$.*\"}\],' \
                            ' \"recipe\": \[\],' \
                            ' \"recipe_ingredient\": \[\],' \
                            ' \"waiting_recipe\": \[\],' \
                            ' \"waiting_recipe_ingredient\": \[\]}'

    def test_users_created_and_other_tables_are_empty(self):
        result = dump_backup()
        print(result)  # TODO
        match = re.fullmatch(self.user_pattern, result)
        self.assertTrue(match)
