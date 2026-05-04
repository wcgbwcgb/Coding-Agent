def find_Product(arr,n):
    res = 1
    for x in set(arr):
        res *= x
    return res
