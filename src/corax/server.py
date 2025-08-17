import socket


if __name__ == "__main__":
    public_conn = socket.create_server(
        ("", 2004),
        family=socket.AF_INET6,
        dualstack_ipv6=True
    )
    public_conn.listen()
    conn, addr = public_conn.accept()
    print("Connection:", conn)
    print("Address of the client:", addr)
