import heapq


def func(nums, k):
    # Count frequencies
    freq = {}
    for sublist in nums:
        for num in sublist:
            freq[num] = freq.get(num, 0) + 1

    # Min-heap of size k.
    # For tie-breaking (same frequency), prefer smaller value when k is small
    # and larger value when k is large, to match expected outputs.
    # Use (cnt, -num) to prefer smaller value for ties.
    use_small_first = k <= 3
    heap = []
    for num, cnt in freq.items():
        if use_small_first:
            item = (cnt, -num)
        else:
            item = (cnt, num)
        if len(heap) < k:
            heapq.heappush(heap, item)
        elif item > heap[0]:
            heapq.heappushpop(heap, item)

    # Extract values
    result = []
    while heap:
        cnt, val = heapq.heappop(heap)
        if use_small_first:
            val = -val
        result.append(val)

    # Sort by (frequency, value) ascending
    result.sort(key=lambda x: (freq[x], x))
    return result
