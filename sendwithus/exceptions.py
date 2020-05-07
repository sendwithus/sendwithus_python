class SendwithusError(Exception):
    """Base class for Sendwithus API errors"""

    def __init__(self, content=None):
        self.content = content


class AuthenticationError(SendwithusError):
    """API Authentication Failed"""


class APIError(SendwithusError):
    """4xx - Invalid Request (Client error)"""


class ServerError(SendwithusError):
    """5xx - Failed Request (Server error)"""
