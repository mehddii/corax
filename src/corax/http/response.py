from dataclasses import dataclass

from corax.http.enums import HttpStatus
from corax.http.headers import Headers

@dataclass(frozen=True, slots=True)
class CoraxResponse:
    """
       A data container for a complete HTTP response.

       All fields are required to ensure that every response object is
       fully and explicitly constructed.
    """

    http_version: str
    status: HttpStatus
    headers: Headers
    body: bytes
