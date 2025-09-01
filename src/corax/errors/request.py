class InvalidRequest(Exception):
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = "Request has an invalid format, either first line or the headers weren't provided!"
        super().__init__(message)
