def max_Prime_Factors (n):
    # Find the largest prime factor of n
    # Handle factor 2
    largest = 2
    while n % 2 == 0:
        largest = 2
        n //= 2
    # Check odd factors up to sqrt(n)
    factor = 3
    while factor * factor <= n:
        while n % factor == 0:
            largest = factor
            n //= factor
        factor += 2
    # If n is still greater than 1, it is a prime factor itself
    if n > 1:
        largest = n
    return largest
