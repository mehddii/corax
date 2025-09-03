from corax.http.response import CoraxResponse


class ResponseSerializer:
    """
        Serializes a CoraxResponse object into a raw byte-string.
    """
    def __init__(self, response: CoraxResponse):
        self.response: CoraxResponse = response

    def serialize(self) -> bytes:
        """
            Builds the full HTTP response as a single bytes object.
        """
        raw_start_line = self._build_start_line()
        raw_headers = self._build_headers()
        raw_body = self.response.body

        return b"\r\n".join([
            raw_start_line,
            raw_headers,
            raw_body
        ])

    def _build_start_line(self) -> bytes:
        """
            Constructs the status-line of the HTTP response.
        """
        http_version = self.response.http_version
        status_code = self.response.status.code
        status_phrase = self.response.status.phrase
        start_line = f"HTTP/{http_version} {status_code} {status_phrase}"

        return start_line.encode("utf-8")

    def _build_headers(self) -> bytes:
        """
            Constructs the header block of the response.
        """
        headers = self.response.headers
        headers_list = []

        for key in headers:
            for value in headers.get_all(key):
                header = ": ".join([key, value])
                headers_list.append(header.encode("utf-8"))

        raw_headers = b"\r\n".join(headers_list)
        raw_headers += b"\r\n"
        return raw_headers
