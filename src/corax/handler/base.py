from abc import ABC, abstractmethod

from corax.http.request import CoraxRequest
from corax.http.response import CoraxResponse


class BaseHandler(ABC):
    """
        Defines the interface for all request handlers.

        A handler's primary responsibility is to process a request and
        produce a corresponding response.
    """
    @abstractmethod
    def handle(self, request: CoraxRequest) -> CoraxResponse:
        """
            Processes an incoming request and returns a response.
        """
        pass
