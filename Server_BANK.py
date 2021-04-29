import socket
import threading
import sqlite3


connections = []
addresses = []


def add_user(username, password, pin):
    db_connection = sqlite3.connect('bank_accounts.db')
    cursor = db_connection.cursor()
    check = "SELECT * FROM bank_accounts WHERE username = " + '"' + username + '"'
    cursor.execute(check)
    selected_player = cursor.fetchone()
    if selected_player:
        return "User Already Exists."
    try:
        cursor.execute("INSERT INTO bank_accounts VALUES (:username, :password, :balance, :pin_code, :occupied)",
                       {'username': username, 'password': password, 'balance': 0, 'pin_code': int(pin), 'occupied': 0})
        db_connection.commit()
        db_connection.close()
        print("Account was Created Successfully.")
        return "Account was Created Successfully."
    except:
        return "Error"



def deposit(current_info, money, current_account):
    current_balance = current_info[2]
    current_balance += money
    current_account.update_account_balance(current_balance)
    return "Successfully Deposited " + str(money) + " Into Your Bank Account."


def withdraw(current_info, money, current_account):
    current_balance = current_info[2]
    if current_balance >= money:
        current_balance -= money
        current_account.update_account_balance(current_balance)
        return "Successfully Withdrew " + str(money) + " From Your Bank Account."
    else:
        return "Couldn't Perform Operation, Insufficient Balance in Your Account, Withdrawal Failed."


class Account:
    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

    def log_into_account(self, username, password):
        if self.is_available():
            try:
                db_connection = sqlite3.connect('bank_accounts.db')
                cursor = db_connection.cursor()
                cursor.execute("SELECT * FROM bank_accounts WHERE username = " + '"' + username + '"')
                selected_player = cursor.fetchone()
                if password == selected_player[1]:
                    cursor.execute("""UPDATE bank_accounts SET occupied = :occupied
                                                         WHERE username = :username""",
                                   {'occupied': 1, 'username': username})
                    db_connection.commit()
                    db_connection.close()
                    return "Successfully Logged into Account."
                else:
                    return "Incorrect Credentials Were Given, Try Again..."
            except:
                return "Error! User not found"
        else:
            return username + " is unavailable right now, try again later"

    def get_balance(self):
        try:
            db_connection = sqlite3.connect('bank_accounts.db')
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM bank_accounts WHERE username = :username", {'username': self.user_name})
            my_balance = cursor.fetchone()
            return my_balance
        except:
            return "error"

    def is_available(self):
        try:
            db_connection = sqlite3.connect('bank_accounts.db')
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM bank_accounts WHERE username = :username", {'username': self.user_name})
            return cursor.fetchone()[4] == 0
        except:
            return "error"

    def disconnect_from_account(self):
        try:
            db_connection = sqlite3.connect('bank_accounts.db')
            cursor = db_connection.cursor()
            cursor.execute("""UPDATE bank_accounts SET occupied = :occupied
                                                 WHERE username = :username""",
                           {'occupied': 0, 'username': self.user_name})
            db_connection.commit()
            db_connection.close()
            self.user_name = ""
            self.password = ""
            return self.user_name + " is Now Disconnected."
        except:
            return "error"

    def get_user_name(self):
        return self.user_name

    def validate_pin_code(self, pin):
        try:
            db_connection = sqlite3.connect('bank_accounts.db')
            cursor = db_connection.cursor()
            str1 = "SELECT * FROM bank_accounts WHERE username = " + '"' + self.user_name + '"'
            cursor.execute(str1)
            details = cursor.fetchone()
            return details[3] == pin
        except:
            print("error")

    def update_account_balance(self, new_balance):
        try:
            db_connection = sqlite3.connect('bank_accounts.db')
            cursor = db_connection.cursor()
            str1 = "SELECT * FROM bank_accounts WHERE username = " + '"' + self.user_name + '"'
            cursor.execute(str1)

            cursor.execute("""UPDATE bank_accounts SET balance = :new_balance
                                     WHERE username = :username""",
                           {'new_balance': new_balance, 'username': self.user_name})
            db_connection.commit()
            db_connection.close()
        except:
            print("Error!")


def client_tui(connection, current_account):
    instructions = "1 - Log in to Account\n2 - Register a New Account\n3 - Deposit Funds to Your Account\n4 - " \
                   "Withdraw Funds From Your Account\n5 - Display Balance\n6 - Disconnect From Account "
    try:
        connection.send(bytes(instructions, "UTF-8"))
        current_account = Account("", "")
        while True:
            client_response = connection.recv(1024).decode("UTF-8")
            print("Response from ATM (Client): ", client_response)
            if client_response == "1":  # login
                connection.send(bytes("Enter a Username -", "UTF-8"))
                username = connection.recv(1024).decode("UTF-8")
                connection.send(bytes("Enter a Password -", "UTF-8"))
                password = connection.recv(1024).decode("UTF-8")
                current_account = Account(username, password)
                answer = current_account.log_into_account(username, password)
                connection.send(bytes(answer, "UTF-8"))
            elif client_response == "2":  # register
                connection.send(bytes("Enter a Username -", "UTF-8"))
                username = connection.recv(1024).decode("UTF-8")
                connection.send(bytes("Enter a Password -", "UTF-8"))
                password = connection.recv(1024).decode("UTF-8")
                connection.send(bytes("Enter a PIN Code -", "UTF-8"))
                pin = connection.recv(1024).decode("UTF-8")
                answer = add_user(username, password, pin)
                connection.send(bytes(answer, "UTF-8"))
            elif client_response == "3":  # deposit
                if current_account.get_user_name() == "":
                    connection.send(bytes("Error! Not connected to a Bank Account.", "UTF-8"))
                else:
                    connection.send(bytes("Enter a PIN Code -", "UTF-8"))
                    pin = connection.recv(1024).decode("UTF-8")
                    if pin.isdigit() and current_account.validate_pin_code(int(pin)):
                        connection.send(bytes("Enter Amount of Money to Deposit -", "UTF-8"))
                        to_deposit = connection.recv(1024).decode("UTF-8")
                        if to_deposit.isdigit():
                            answer = deposit(current_account.get_balance(), float(to_deposit), current_account)
                        else:
                            answer = "Invalid Input"
                        connection.send(bytes(answer, "UTF-8"))
                    else:
                        connection.send(bytes("Incorrect PIN Code!", "UTF-8"))
            elif client_response == "4":  # withdraw
                if current_account.get_user_name() == "":
                    connection.send(bytes("Error! Not connected to a Bank Account.", "UTF-8"))
                else:
                    connection.send(bytes("Enter a PIN Code -", "UTF-8"))
                    pin = connection.recv(1024).decode("UTF-8")
                    if pin.isdigit() and current_account.validate_pin_code(int(pin)):
                        connection.send(bytes("Enter an Amount of Money to Withdraw -", "UTF-8"))
                        to_withdraw = connection.recv(1024).decode("UTF-8")
                        if to_withdraw.isdigit():
                            answer = withdraw(current_account.get_balance(), float(to_withdraw), current_account)
                        else:
                            answer = "Invalid Input"
                        connection.send(bytes(answer, "UTF-8"))
                    else:
                        connection.send(bytes("Incorrect PIN Code!", "UTF-8"))
            elif client_response == "5":  # display balance
                connection.send(bytes(str(current_account.get_balance()[2]), "UTF-8"))
            elif client_response == "6":  # disconnect
                if current_account.get_user_name() == "":
                    connection.send(bytes("Error! Not connected to a Bank Account.", "UTF-8"))
                else:
                    print(current_account.disconnect_from_account())
                    connection.send(bytes("Logged Out Successfully.\n" + instructions, "UTF-8"))
            else:
                connection.send(bytes("Unknown Command.", "UTF-8"))
    except ConnectionResetError:
        print(current_account.disconnect_from_account())


def start_connection_thread(conn, address):
    t = threading.Thread(target=client_tui, args=(conn, address,))
    t.start()


def connect_to_clients(server_socket):
    while 1:
        conn, address = server_socket.accept()
        connections.append(conn)
        addresses.append(address)
        print(address[0], "is now Connected.")
        start_connection_thread(conn, address)


def start_server():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 1789))
    server_socket.listen(1)
    print("Waiting For Connection...\n")
    connect_to_clients(server_socket)

def main():
    start_server()



if __name__ == '__main__':
    main()
