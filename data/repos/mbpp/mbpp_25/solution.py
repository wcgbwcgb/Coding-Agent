from collections import Counter

def find_Product(arr,n):
    freq = Counter(arr)
    prod = 1
    for num, cnt in freq.items():
        if cnt == 1:
            prod *= num
    return prod
