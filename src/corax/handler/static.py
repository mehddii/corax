from pathlib import Path

from corax.handler.base import BaseHandler
from corax.http.enums import HttpStatus
from corax.http.headers import Headers
from corax.http.request import CoraxRequest
from corax.http.response import CoraxResponse

class StaticHandler(BaseHandler):
    """
        A request handler that serves static files from a root directory.
    """
    def __init__(self, base_folder: str | Path) -> None:
        """
            Initializes the handler with a specific root directory.
        """
        self.base_folder: Path = Path(base_folder).resolve()

        if not self.base_folder.exists():
            self.base_folder.mkdir()
        elif not self.base_folder.is_dir():
            raise FileNotFoundError(f"Root directory '{self.base_folder}' is not a directory.")

    def handle(self, request: CoraxRequest) -> CoraxResponse:
        """
            Handles a request by attempting to find and serve a static file.
        """
        uri = request.uri
        http_version = request.http_version
        file_path = self._get_safe_path(uri)

        if file_path is None:
            return self._not_found(http_version)

        return self._serve_file(file_path, http_version)

    def _serve_file(self, file_path: Path, http_version: str) -> CoraxResponse:
        """
            Creates a 200 OK response with the contents of a given file.
        """
        body = file_path.read_bytes()
        headers = Headers()
        headers["Content-Length"] = str(len(body))

        return CoraxResponse(
            http_version,
            HttpStatus.OK,
            headers,
            body
        )

    def _not_found(self, http_version: str) -> CoraxResponse:
        """
            Creates a standard 404 Not Found response.
        """
        body = b"<h1>404 Not Found</h1>"
        headers = Headers()
        headers["Content-Length"] = str(len(body))
        headers["Content-Type"] = "text/html"

        return CoraxResponse(
            http_version,
            HttpStatus.NOT_FOUND,
            headers,
            body
        )

    def _get_safe_path(self, uri: str) -> Path | None:
        """
            Resolves a request URI to a safe, validated file path.
        """
        path = self._sanitize_uri(uri)

        if path is not None and path.is_dir():
            path /= "index.html"

        if path is None or not self._validate_path(path):
            return None

        return path

    def _sanitize_uri(self, uri: str) -> Path | None:
        """
            Converts a URI string to a resolved absolute path.
        """
        if not uri.startswith("/"):
            return None

        uri = uri.removeprefix("/")
        path = self.base_folder / Path(uri)
        return path.resolve()

    def _validate_path(self, path: Path) -> bool:
        """
            Validates that a path is a file and is safely within the base folder.
        """
        base = self.base_folder.resolve()

        try:
            return path.is_relative_to(base) and path.exists() and path.is_file()
        except ValueError:
            return False
