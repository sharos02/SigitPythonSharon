def sum_numbers():
    """ Exercise 1-a """
    # Function returns the sum of the inputted numbers
    sum = 0
    to_add = input('1-a) Enter a number (Quit with "stop"): ')
    while to_add.lower() != "stop":
        if to_add.isdigit():
            sum += int(to_add)
        to_add = input('     Enter a number (Quit with "stop": ')
    return sum


def sum_list_numbers():
    """ Exercise 1-b """
    # Function returns the sum of the numbers entered as a list
    sum = 0
    num_list = input("Enter a list of numbers in the following format -> a, b, c, d: ").split(",")
    try:
        for num in num_list:
            sum += int(num)
    except ValueError:
        return "Value Error -> Invalid Input"
    return sum


def check_xo_win(mat):
    """ Exercise 2 """
    # Function gets a matrix (board of tic-tac-toe)
    # Function prints which player won the game
    print("2) ", end="")
    if mat[0][0] == mat[0][1] == mat[0][1] == 1 or mat[1][0] == mat[1][1] == mat[1][2] == 1 or \
            mat[2][0] == mat[2][1] == mat[2][2] == 1:
        print("Result: Player #1 is the Winner!")
    elif mat[0][0] == mat[1][0] == mat[2][0] == 1 or mat[1][0] == mat[1][1] == mat[1][2] == 1 or \
            mat[0][2] == mat[1][2] == mat[2][2] == 1:
        print("Result: Player #1 is the Winner!")
    elif mat[0][0] == mat[1][1] == mat[2][2] == 1 or mat[2][0] == mat[1][1] == mat[2][0] == 1:
        print("Result: Player #1 is the Winner!")
    elif mat[0][0] == mat[0][1] == mat[0][2] == 2 or mat[1][0] == mat[1][1] == mat[1][2] == 2 or \
            mat[2][0] == mat[2][1] == mat[2][2] == 2:
        print("Result: Player #2 is the Winner!")
    elif mat[0][0] == mat[1][0] == mat[2][0] == 2 or mat[1][0] == mat[1][1] == mat[2][1] == 2 or \
            mat[0][2] == mat[1][2] == mat[2][2] == 2:
        print("Result: Player #2 is the Winner!")
    elif mat[0][0] == mat[1][1] == mat[2][2] == 2 or mat[2][0] == mat[1][1] == mat[0][2] == 2:
        print("Result: Player #2 is the Winner!")
    else:
        print("Result: Tie")


def compress_string():
    """ Exercise 3 """
    # Function returns the compressed string of the inputted expression
    to_compress = input("Enter an expression: ")
    compressed_string = ""
    count = 0
    if len(to_compress) > 1:
        for i in range(len(to_compress) - 1):
            count += 1
            if to_compress[i] != to_compress[i + 1]:
                compressed_string += to_compress[i] + str(count)
                count = 0
        if to_compress[-1] != to_compress[-2]:
            compressed_string += to_compress[-1] + str(1)
            return compressed_string
        if to_compress[i] == to_compress[i - 1]:
            count += 1
            compressed_string += to_compress[i] + str(count)
        else:
            count = 1
            compressed_string += to_compress[i + 1] + str(count)
    else:
        compressed_string += to_compress + str(1)
    return compressed_string


def check_id():
    """ Exercise 4 """
    # Function prints if the inputted ID number is valid
    id = input("4) Enter ID number: ")
    sum = 0
    factor = 1
    if id.isdigit() and 0 < len(id) <= 9:
        for i in range(len(id) - 1):
            temp = int(id[i]) * factor
            if temp > 9:
                temp = temp % 10 + int(temp / 10)
            sum += temp
            if factor == 1:
                factor = 2
            else:
                factor = 1
        if sum % 10 != 0:
            ceiled_num = sum + (10 - sum % 10)
        else:
            ceiled_num = sum
        if ceiled_num - sum == int(id[-1]):
            print("SUCCESS: The ID Number is Valid!")
        else:
            print("FAIL: The ID Number is Invalid!")
    else:
        print("Invalid Input!")


def perform(value):
    """ Exercise 5 """
    return value / 2


def map_function(array, function_name):
    """ Exercise 5 """
    return [function_name(val) for val in array]


def main():
    print("Sum of the entered number: ", sum_numbers())
    print("1-b) Sum of the entered numbers: ", sum_list_numbers())
    check_xo_win([[1, 2, 0], [2, 1, 0], [2, 1, 1]])
    print("3) The Compressed Expression is: ", compress_string())
    check_id()
    arr = [100, 200, 300, 400]
    print("5) Before Map Function: ", arr)
    arr = map_function(arr, perform)
    print(" After Map Function: ", arr)


if __name__ == "__main__":
    main()
