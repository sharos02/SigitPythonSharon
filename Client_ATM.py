import socket


def main():
    atm_socket = socket.socket()
    atm_socket.connect(('127.0.0.1', 1789))
    print("Successfully Connected to the Bank...")
    bank_reply = atm_socket.recv(1024).decode("UTF-8")
    print(bank_reply)
    while True:
        send_to_bank = input("Your Choice: ")
        atm_socket.send(bytes(send_to_bank, "UTF-8"))
        bank_reply = atm_socket.recv(1024).decode("UTF-8")
        print(bank_reply)


if __name__ == '__main__':
    main()
