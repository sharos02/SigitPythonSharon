import socket


def main():
    my_socket = socket.socket()
    my_socket.connect(('127.0.0.1', 1789))
    from_bank = my_socket.recv(1024).decode()
    print("Bank's Message: ", from_bank)
    data_to_bank = input("")
    my_socket.send(bytes(data_to_bank.encode()))
    while data_to_bank.lower() != "stop":
        from_bank = my_socket.recv(1024).decode("UTF-8")
        print(str(from_bank))
        data_to_bank = input("")
        data_to_bank = my_socket.send(data_to_bank.encode())
    my_socket.close()


if __name__ == "__main__":
    main()
