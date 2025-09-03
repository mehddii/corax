import socket
import logging
from dataclasses import replace

from corax.handler.static import StaticHandler
from corax.http.parser import RequestParser
from corax.http.serializer import ResponseSerializer
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

        handler = StaticHandler("./www")
        logger.debug(f"Serving static files from {handler.base_folder}")

        while True:
            client_connection: socket.socket
            client_address: tuple[str, int, str, str]
            client_connection, client_address = connection.accept()
            logger.debug(f"{client_connection}, {client_address}")

            try:
                buffer = b""
                separator = b"\r\n\r\n"
                while True:
                    data = client_connection.recv(1024)
                    buffer += data

                    if separator in buffer:
                        break

                header_end_index = buffer.find(separator)
                raw_request_head = buffer[:header_end_index + len(separator)]
                body_so_far = buffer[header_end_index + len(separator):]

                request_parser = RequestParser(raw_request_head)
                request = request_parser.parse()
                logger.info(f"Received request: {request.method.value} {request.uri}")

                content_length = request.headers.get("Content-Length")
                if  content_length is not None:
                    data_size = int(content_length)
                    unread_data_size = data_size - len(body_so_far)

                    body = body_so_far
                    if unread_data_size > 0:
                        data = client_connection.recv(unread_data_size)
                        body += data

                    request = replace(request, body=body)

                logger.debug(f"Request body received: {request.body.decode('utf-8', 'ignore') or 'No body'}")

                response = handler.handle(request)
                serializer = ResponseSerializer(response)
                raw_response = serializer.serialize()
                client_connection.sendall(raw_response)
                logger.info(f"Response sent: {response.status.code} {response.status.phrase}")
            except Exception as e:
                logger.error(f"Error handling connection: {e}")
            finally:
                client_connection.close()
                logger.debug("Connection with the client closed successfully")
    except KeyboardInterrupt:
        logger.info("Shutting down the server...")
    finally:
        connection.close()

if __name__ == "__main__":
   start()
