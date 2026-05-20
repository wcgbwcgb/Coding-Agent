def rev(num):
    return int(str(num)[::-1])


def check(num):
    return num == 2 * rev(num) - 1
