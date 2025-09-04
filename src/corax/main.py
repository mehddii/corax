import logging

from corax.config.logging import setup_logging
from corax.handler.static import StaticHandler
from corax.server import CoraxServer

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
    handler = StaticHandler("./www")

    server = CoraxServer(host, port, handler)
    server.main_loop()

if __name__ == "__main__":
   start()
