class CacheDecorator(dict):
    def __init__(self, func_name):
        """ Constructor """
        self.func_name = func_name

    def __call__(self, *args):
        """ Return result of function call if cached"""
        return self[args]

    def __missing__(self, key):
        """ Return result of function call and cache the result """
        result = self[key] = self.func_name(*key)
        return result


@CacheDecorator
def factorial(num):
    """
    Function gets an integer number
    Function returns the factorial (num!) of the given number
    """
    if num is int:
        if num == 0 or num == 1:
            return 1
        return num * factorial(num - 1)


def main():
    print("Factorial: ", factorial(5))
    print("Cached Results: ", factorial)  # all factorials from 1 to 5 are cached
    print("Factorial: ", factorial(3))


if __name__ == "__main__":
    main()
