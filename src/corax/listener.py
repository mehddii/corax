import socket
import logging

from .errors.socket import (
    SocketConnectionOFF,
    SocketConnectionON,
)

logger = logging.getLogger(__name__)

class SocketListener:
    """
        Manages the lifecycle of a TCP socket.

        This class is an abstraction for the socket that only listen for
        requests, accept connections and hand them off to a connection
        handler.
    """

    host: str
    port: int
    family: socket.AddressFamily
    dualstack_ipv6: bool
    public_connection: socket.socket | None

    def __init__(
        self,
        address: tuple[str, int],
        family: socket.AddressFamily = socket.AF_INET6,
        dualstack_ipv6: bool = True
    ) -> None:
        """
            Initializes the SocketListener with a given address, supports
            ipv6 by default.
        """

        self.host, self.port = address
        self.family = family
        self.dualstack_ipv6 = dualstack_ipv6
        self.public_connection: socket.socket | None = None

    def start(self) -> None:
        """
            Create a TCP socket, bind it to an address and listen to incoming connections.
        """
        if self.public_connection is not None:
            raise SocketConnectionON()

        self.public_connection = socket.create_server(
            (self.host, self.port),
            family=self.family,
            dualstack_ipv6=self.dualstack_ipv6
        )

    def accept(self) -> tuple[socket.socket, tuple[str, int, str, str]]:
        """
            Accepts new client connections.
        """

        if self.public_connection is None:
            raise SocketConnectionOFF()

        return self.public_connection.accept()

    def close (self, tries: int = 3) -> None:
        """
            Closes the listening socket gracefully.
        """

        if self.public_connection is None:
            return

        for t in range(tries):
            try:
                self.public_connection.close()
            except OSError:
                logger.warning("Connection could not be close due to an unknown error")
                if t < tries - 1:
                    logger.warning("Trying to close the socket again...")
                elif t == tries - 1:
                    raise OSError

        self.public_connection = None
