import socket

class SocketConnectionOFF(Exception):
    def __init__(self, message=None):
        if message == None:
            message = "No public connection is captured, check that your server is starting!"
        super().__init__(message)

class SocketConnectionON(Exception):
    def __init__(self, message=None):
        if message == None:
            message = "A public connection already running!"
        super().__init__(message)


class SocketListener:
    def __init__(
        self,
        address,
        family=socket.AF_INET6,
        dualstack_ipv6=True
    ):
        self.host, self.port = address
        self.family = family
        self.dualstack_ipv6 = dualstack_ipv6
        self.public_connection = None

    def start(self):
        if self.public_connection != None:
            raise SocketConnectionON

        self.public_connection = socket.create_server(
            (self.host, self.port),
            family=self.family,
            dualstack_ipv6=self.dualstack_ipv6
        )

    def accept(self):
        if self.public_connection == None:
            raise SocketConnectionOFF()

        return self.public_connection.accept()

    def close (self, tries=3):
        if self.public_connection == None:
            return

        for t in range(tries):
            try:
                self.public_connection.close()
            except OSError:
                print("Connection could not be close due to an unknown error")
                if t < tries - 1:
                    print("Trying to close the socket again...")
                elif t == tries - 1:
                    raise OSError

        self.public_connection = None
