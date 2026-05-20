

def prime_fib(n: int):
    """
    prime_fib returns n-th number that is a Fibonacci number and it's also prime.
    >>> prime_fib(1)
    2
    >>> prime_fib(2)
    3
    >>> prime_fib(3)
    5
    >>> prime_fib(4)
    13
    >>> prime_fib(5)
    89
    """
    def is_prime(num: int) -> bool:
        if num < 2:
            return False
        if num % 2 == 0:
            return num == 2
        i = 3
        while i * i <= num:
            if num % i == 0:
                return False
            i += 2
        return True

    a, b = 1, 2  # F2=1, F3=2 (first candidate after 1)
    count = 0
    while True:
        if is_prime(b):
            count += 1
            if count == n:
                return b
        a, b = b, a + b
