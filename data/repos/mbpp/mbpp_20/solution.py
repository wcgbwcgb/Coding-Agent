def is_woodall(x):
    if x <= 0:
        return False
    n = 1
    while True:
        woodall = n * (1 << n) - 1
        if woodall == x:
            return True
        if woodall > x:
            return False
        n += 1
