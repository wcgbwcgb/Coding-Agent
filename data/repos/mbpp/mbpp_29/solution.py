def get_Odd_Occurrence(arr,arr_size):
    result = 0
    for x in arr:
        result ^= x
    return result
