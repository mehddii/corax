import socket
import logging

import corax.listener as listener
from corax.config.logging import setup_logging

logger = logging.getLogger(__name__)

def dev() -> None:
    setup_logging("DEBUG")
    main()

def start() -> None:
    setup_logging()
    main()

def main() -> None:
    host: str = "::"
    port: int = 2004
    connection: listener.SocketListener = listener.SocketListener((host, port))
    try:
        connection.start()
        logger.info(f"Server started running on port {port}")

        while True:
            client_connection: socket.socket
            client_address: tuple[str, int, str, str]
            client_connection, client_address = connection.accept()
            logger.debug(f"{client_connection}, {client_address}")
            client_connection.close()

    except KeyboardInterrupt:
        logger.info("Shutting down the server...")

    finally:
        connection.close()

if __name__ == "__main__":
   start()
