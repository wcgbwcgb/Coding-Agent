def find_Sum(arr,n):
    freq = {}
    for x in arr:
        freq[x] = freq.get(x, 0) + 1
    total = 0
    for x, count in freq.items():
        if count > 1:
            total += x * count
    return total
