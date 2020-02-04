class WrongPageLoadedError(Exception):
    def __init__(self, expected=None, actual=None):
        message = "Wrong page loaded."
        if expected:
            message += " Expected: %s. " % expected
        if actual:
            message += " Actual: %s. " % actual
        super().__init__(message)
