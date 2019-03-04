

class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class UnknownServiceError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

