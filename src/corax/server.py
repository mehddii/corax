import socket
import logging

from corax.connection import ConnectionHandler
from corax.handler.base import BaseHandler
from corax.handler.static import StaticHandler
import corax.listener as listener

logger = logging.getLogger(__name__)

class CoraxServer:
    host: str
    port: int
    handler: BaseHandler
    connection: listener.SocketListener

    def __init__(self, host: str, port: int, handler: BaseHandler) -> None:
        self.host = host
        self.port = port
        self.handler = handler
        self.connection = listener.SocketListener((host, port))

    def main_loop(self) -> None:
        try:
            self.connection.start()
            logger.info(f"Server started running on port {self.port}")

            if isinstance(self.handler, StaticHandler):
                logger.debug(f"Serving static files from {self.handler.base_folder}")

            while True:
                client_connection: socket.socket
                client_address: tuple[str, int, str, str]
                client_connection, client_address = self.connection.accept()
                logger.debug(f"{client_connection}, {client_address}")

                connection_handler = ConnectionHandler(
                    client_connection,
                    client_address,
                    self.handler
                )
                connection_handler.handle()
        except KeyboardInterrupt:
            logger.info("Shutting down the server...")
        finally:
            self.connection.close()
