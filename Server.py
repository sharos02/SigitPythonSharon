import socket


def main():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 1789))
    server_socket.listen(1)
    (client_socket, client_address) = server_socket.accept()
    msg = "Connection Successful"
    to_client = client_socket.send(bytes(msg.encode()))
    data = server_socket.recv(1024)
    data = data.decode()
    print(str(data))
    while data.lower() != "stop":
        to_client = client_socket.send(bytes(msg.encode()))
        data = server_socket.recv(1024).decode("UTF-8")
        print(str(data))

    server_socket.close()


if __name__ == "__main__":
    main()

