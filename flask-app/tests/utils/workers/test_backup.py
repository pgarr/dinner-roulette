import datetime
import re
from unittest.mock import patch, Mock, ANY

import pytest

from app.utils.workers import backup
from app.utils.workers.backup import BackupScheduler

user_pattern = r'{\"user\": \[{\"id\": 1, \"username\": \"test\", \"email\": \"test@test\.com\", \"password_hash\":' \
               r' \"pbkdf2:sha256:150000\$.*\"}, {\"id\": 2, \"username\": \"test2\", \"email\": \"test2@test\.com\",' \
               r' \"password_hash\": \"pbkdf2:sha256:150000\$.*\"}, {\"id\": 3, \"username\": \"admin\", \"email\":' \
               r' \"admin@test\.com\", \"password_hash\": \"pbkdf2:sha256:150000\$.*\"}\],'


@pytest.fixture
def backup_scheduler(database):
    return BackupScheduler(10000)


@pytest.fixture
def recipes_set(test_client, database, users_set, make_recipe):
    user1, user2, admin = users_set

    recipe_model = make_recipe(title='test', time=1, difficulty=1, link='http://test.com', preparation='test',
                               author=user1, create_date=datetime.datetime(2019, 1, 30),
                               last_modified=datetime.datetime(2019, 11, 1),
                               ingredients=[{'title': 'test1', 'amount': 1, 'unit': 'kg'},
                                            {'title': 'test2', 'amount': 1, 'unit': 'kg'}])
    recipe_model_2 = make_recipe(title='test2', time=2, difficulty=2, link='http://test2.com', preparation='test',
                                 author=user2, create_date=datetime.datetime(2019, 1, 30),
                                 last_modified=datetime.datetime(2019, 11, 1),
                                 ingredients=[{'title': 'test1', 'amount': 2, 'unit': 'kg'},
                                              {'title': 'test2', 'amount': 2, 'unit': 'dag'}])

    return user1, user2, admin, recipe_model, recipe_model_2


def test_backup_users_created_and_other_tables_are_empty(test_client, database, backup_scheduler, users_set):
    result = backup_scheduler.dump_backup()

    pattern = user_pattern + r' \"recipe\": \[\], \"recipe_ingredient\": \[\]}'

    match = re.fullmatch(pattern, result)
    assert match


def test_backup_users_created_and_populated_all_tables(test_client, database, backup_scheduler, recipes_set,
                                                       make_recipe):
    user1, user2, admin, recipe1, recipe2 = recipes_set

    result = backup_scheduler.dump_backup()

    pattern = user_pattern + r' \"recipe\": \[{\"id\": 1, \"title\": \"test\", \"time\": 1, \"difficulty\": 1, ' \
                             r'\"link\": \"http://test\.com\", \"preparation\": \"test\", \"create_date\": ' \
                             r'\"2019-01-30 00:00:00\", \"last_modified\": \"2019-11-01 00:00:00\",' \
                             r' \"author_id\": 1, "status": "pending"}, {\"id\": 2, \"title\": \"test2\",' \
                             r' \"time\": 2, \"difficulty\": 2, \"link\": \"http://test2\.com\", \"preparation\": ' \
                             r'\"test\", \"create_date\": \"2019-01-30 00:00:00\", \"last_modified\": ' \
                             r'\"2019-11-01 00:00:00\", \"author_id\": 2, "status": "pending"}], ' \
                             r'\"recipe_ingredient\": \[{\"id\": 1, \"title\": \"test1\", \"amount\": 1\.0, ' \
                             r'\"unit\": \"kg\", \"recipe_id\": 1}, {\"id\": 2, \"title\": \"test2\", ' \
                             r'\"amount\": 1\.0, \"unit\": \"kg\", \"recipe_id\": 1}, {\"id\": 3, \"title\": ' \
                             r'\"test1\", \"amount\": 2\.0, \"unit\": \"kg\", \"recipe_id\": 2}, {\"id\": 4, ' \
                             r'\"title\": \"test2\", \"amount\": 2\.0, \"unit\": \"dag\", \"recipe_id\": 2}\]}'

    match = re.fullmatch(pattern, result)
    assert match


def test_send_calls_send_email(backup_scheduler):
    dmp = '{"mockup": "mockup"}'
    backup.send_email = Mock()
    fake_now = datetime.date(2019, 1, 1)
    with patch("datetime.date") as dt:
        dt.today.return_value = fake_now
        backup_scheduler.send(dmp)
    dt.today.assert_called_once_with()
    backup.send_email.assert_called_once_with(subject="Test January 01, 2019",
                                              attachments=[("Dump.json", "application/json", dmp)], html_body=None,
                                              recipients=ANY, sender=ANY, text_body=None)
