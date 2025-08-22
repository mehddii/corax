import socket

import corax.listener as listener

def main() -> None:
    connection: listener.SocketListener = listener.SocketListener(("::", 2004))
    try:
        connection.start()

        while True:
            client_connection: socket.socket
            client_address: tuple[str, int, str, str]
            client_connection, client_address = connection.accept()
            print(client_connection, client_address)
            client_connection.close()

    except KeyboardInterrupt:
        print("Shutting down the server...")

    finally:
        connection.close()

if __name__ == "__main__":
   main()
