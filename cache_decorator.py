class CacheDecorator(dict):
    def __init__(self, func_name):
        """ Constructor """
        self.func_name = func_name

    def __call__(self, *parameters):
        """ Return result of function call if cached """
        return self[parameters]

    def __missing__(self, key):
        """ Return result of function call and cache the result """
        function_result = self[key] = self.func_name(*key)
        return function_result


@CacheDecorator
def factorial(num):
    """
    Function gets an integer number
    Function returns the factorial (num!) of the given number
    """
    if type(num) is int:
        if num == 0 or num == 1:
            return 1
        return num * factorial(num - 1)


def main():
    print("Factorial of 5: ", factorial(5))
    print("Cached Results: ", factorial)  # all factorials from 1 to 5 are cached
    print("Factorial of 3: ", factorial(3))
    print("Cached Results: ", factorial)


if __name__ == "__main__":
    main()
