import socket
import logging
from dataclasses import replace

from corax.handler.base import BaseHandler
from corax.http.parser import RequestParser
from corax.http.request import CoraxRequest
from corax.http.response import CoraxResponse
from corax.http.serializer import ResponseSerializer

logger = logging.getLogger(__name__)

class ConnectionHandler:
    """
        Manages the complete lifecycle of a single client connection.
    """
    def __init__(
        self,
        connection_socket: socket.socket,
        client_address: tuple[str, int, str, str],
        handler: BaseHandler
    ):
        """
            Initializes the handler for a specific client socket.
        """
        self.connection_socket: socket.socket = connection_socket
        self.client_address: tuple[str, int, str, str] = client_address
        self.handler: BaseHandler = handler

    def handle(self) -> None:
        """
            Orchestrates the full request-response cycle for the connection.
        """
        try:
            request = self._read()
            response = self.handler.handle(request)
            self._write(response)
        except Exception as e:
            logger.error(f"Error handling connection: {e}")
        finally:
            self._close()
            logger.debug("Connection with the client closed successfully")

    def _read(self) -> CoraxRequest:
        """
            Reads from the socket and parses the data into a CoraxRequest.
        """
        buffer = b""
        separator = b"\r\n\r\n"
        while True:
            data = self.connection_socket.recv(1024)
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
                data = self.connection_socket.recv(unread_data_size)
                body += data

            request = replace(request, body=body)

        logger.debug(f"Request body received: {request.body.decode('utf-8', 'ignore') or 'No body'}")
        return request

    def _write(self, response: CoraxResponse) -> None:
        """
            Serializes and sends a CoraxResponse to the client.
        """
        serializer = ResponseSerializer(response)
        raw_response = serializer.serialize()
        self.connection_socket.sendall(raw_response)
        logger.info(f"Response sent: {response.status.code} {response.status.phrase}")

    def _close(self) -> None:
        """
            Closes the client connection.
        """
        try:
            self.connection_socket.close()
        except OSError as e:
            logger.warning(f"Ignoring error while closing socket for {self.client_address}: {e}")
