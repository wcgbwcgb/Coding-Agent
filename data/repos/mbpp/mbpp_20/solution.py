def is_woodall(x):
    if x % 2 == 0:
        return False
    if x < 1:
        return False
    n = 1
    while True:
        w = n * (1 << n) - 1
        if w == x:
            return True
        if w > x:
            return False
        n += 1
