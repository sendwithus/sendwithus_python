class SendwithusError(Exception):
    """Base class for Sendwithus-related errors"""


class AuthenticationError(SendwithusError):
    """Errors caused with API keys"""


class APIError(SendwithusError):
    """4xx - Failed Request (Client error)"""


class ServerError(SendwithusError):
    """5xx - Failed Request (Server error)"""
