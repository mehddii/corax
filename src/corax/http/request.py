from dataclasses import dataclass

from corax.http.enums import HttpMethod
from corax.http.headers import Headers

@dataclass(frozen=True, slots=True)
class CoraxRequest:
    """
        A data container for a parsed HTTP request.

        This object holds all the structured information from a raw
        HTTP request, ready to be used by a request handler.
    """
    method: HttpMethod
    uri: str
    http_version: str
    headers: Headers
    body: bytes
