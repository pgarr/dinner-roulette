import re

from app.services.services import get_user_by_email, get_user_by_name


def validate_username(username):
    validator = UsernameValidator(username)
    validator.register("min_length", validator.is_min_length)
    validator.register("unique", validator.is_unique)

    return validator.validate()


def validate_email(email):
    validator = EmailValidator(email)
    validator.register("unique", validator.is_unique)
    validator.register("format", validator.is_email)

    return validator.validate()


def validate_password(password):
    validator = PasswordValidator(password)
    validator.register("min_length", validator.is_min_length)

    return validator.validate()


class AbstractValidator:

    def __init__(self, param):
        self.min_len = 0
        self.max_len = 999
        self.validator_checks = {}
        self.param = param

    def register(self, name, fun):
        self.validator_checks[name] = fun

    def validate(self):
        checks = {}

        for name, fun in self.validator_checks.items():
            result = fun()
            checks[name] = result

        is_valid = all(checks.values())
        return is_valid, checks

    def is_min_length(self):
        return len(self.param) >= self.min_len

    def is_max_length(self):
        return len(self.param) <= self.max_len


class EmailValidator(AbstractValidator):
    def __init__(self, param):
        super().__init__(param)

    def is_unique(self):
        user = get_user_by_email(self.param)
        return user is None

    def is_email(self):
        regex = r'[^@]+@[^@]+\.[^@]+'
        match = re.match(regex, self.param)

        return match is not None


class UsernameValidator(AbstractValidator):
    def __init__(self, param):
        super().__init__(param)
        self.min_len = 3

    def is_unique(self):
        user = get_user_by_name(self.param)
        return user is None


class PasswordValidator(AbstractValidator):
    def __init__(self, param):
        super().__init__(param)
        self.min_len = 6
