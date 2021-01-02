from app.services.auth import get_user_by_name, get_user_by_email


def test_get_user_by_name_existing(users_set):
    user1, user2, admin = users_set
    user = get_user_by_name(user1.username)
    assert user1.__repr__() == user.__repr__()


def test_get_user_by_name_not_existing(users_set):
    user = get_user_by_name('asdfgh')
    assert user is None


def test_get_user_by_email_existing(users_set):
    user1, user2, admin = users_set
    user = get_user_by_email(user1.email)
    assert user1.__repr__() == user.__repr__()


def test_get_user_by_email_not_existing(users_set):
    user = get_user_by_email('asdfgh@fasf.pl')
    assert user is None
