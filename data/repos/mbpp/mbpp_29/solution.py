def get_Odd_Occurrence(arr,arr_size):
    res = 0
    for x in arr:
        res ^= x
    return res
