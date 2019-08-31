class NotLoggedInError(Exception):
    def __init__(self, message="User is not logged in"):
        super().__init__(message)


class UserLoggedInError(Exception):
    def __init__(self, message="User is logged in"):
        super().__init__(message)
