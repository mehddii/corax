from corax.http.enums import HttpMethod
from corax.http.request import CoraxRequest
from corax.http.headers import Headers
from corax.errors.request import InvalidRequest

class RequestParser:
    """
        Parses a raw byte-string into a structured CoraxRequest object.

        This class is responsible for interpreting the HTTP/1.1 protocol,
        handling the request line, headers, and body.
    """
    def __init__(self, raw_request: bytes):
        """
            Initializes the parser with the raw request data.
        """
        self.raw_request: bytes = raw_request
        self.request: CoraxRequest | None = None

    def parse(self) -> CoraxRequest:
        """
            Executes the parsing process and returns an immutable CoraxRequest.

            This method caches its result. Subsequent calls will return the
            same request object without re-parsing.
        """
        if self.request is not None:
            return self.request

        try:
            raw_start_line, raw_headers, raw_body = self._split_request()

            start_line = self._parse_start_line(raw_start_line)
            headers = self._parse_headers(raw_headers)
            body = self._parse_body(raw_body)

            if start_line is None or headers is None:
                raise InvalidRequest()

            method, uri, http_version = start_line
            body = b"" if body is None else body

            request = CoraxRequest(
                method,
                uri,
                http_version,
                headers,
                body
            )
            self.request = request

            return request

        except (ValueError, TypeError):
            raise InvalidRequest("An unexpected error occurred during request parsing.")

    def _split_request(self) -> tuple[bytes, bytes, bytes]:
        """
            Splits the raw request into its three main components.
        """
        try:
            request_head, raw_body = self.raw_request.split(b"\r\n\r\n", 1)
            request_head_lines = request_head.split(b"\r\n")

            raw_start_line = request_head_lines[0]
            raw_headers = b"\r\n".join(request_head_lines[1:])

            return raw_start_line, raw_headers, raw_body
        except ValueError:
            raise InvalidRequest("Malformed request: The header-body separator (\\r\\n\\r\\n) was not found.")

    def _parse_start_line(self, raw_start_line: bytes) -> tuple[HttpMethod, str, str]:
        """
            Parses the request-line into its three components.
        """
        try:
            raw_method, raw_uri, raw_http_version = raw_start_line.split(b" ", 2)
            method = HttpMethod.from_string(raw_method.decode("utf-8"))
            uri = raw_uri.decode("utf-8")
            http_version = raw_http_version.decode("utf-8").split("HTTP/")[1]

            return method, uri, http_version
        except ValueError:
            raise InvalidRequest("Malformed request line: Does not contain three parts.")
        except IndexError:
            raise InvalidRequest("Malformed request line: 'HTTP/' prefix missing from version.")


    def _parse_headers(self, raw_headers: bytes) -> Headers:
        """
            Parses a block of header lines into a Headers object.
        """
        try:
            raw_header_lines = raw_headers.split(b"\r\n")

            headers = Headers()
            for header_line in raw_header_lines:
                if not header_line:
                    continue
                key, value = header_line.decode("utf-8").split(":", 1)
                headers.add(key.strip(), value.strip())

            return headers
        except ValueError:
            raise InvalidRequest("Malformed header line: A header is missing a ':' separator.")

    def _parse_body(self, raw_body: bytes) -> bytes | None:
        """
            Processes the raw body of the request.
        """
        return raw_body
