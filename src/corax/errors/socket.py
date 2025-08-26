class SocketConnectionOFF(Exception):
    def __init__(self, message: str | None = None):
        if message is None:
            message = "No public connection is captured, check that your server is starting!"
        super().__init__(message)

class SocketConnectionON(Exception):
    def __init__(self, message: str | None = None):
        if message is None:
            message = "A public connection already running!"
        super().__init__(message)
