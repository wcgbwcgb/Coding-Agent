from collections import Counter

def freq_element(nums):
    return dict(Counter(elem for sublist in nums for elem in sublist))
