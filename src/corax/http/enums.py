from enum import Enum

class HttpMethod(str, Enum):
    """
        An enumeration for standard HTTP request methods.

        Inherits from `str` to provide string-like behavior.
    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"

    @classmethod
    def from_string(cls, method: str) -> "HttpMethod":
        """
            Case-insensitively creates an HttpMethod from a string.
        """
        try:
            return cls[method.upper()]
        except KeyError:
            raise ValueError(f"'{method}' is not a valid HttpMethod.")
