def find_gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def get_gcd(arr):
    result = arr[0]
    for num in arr[1:]:
        result = find_gcd(result, num)
    return result
