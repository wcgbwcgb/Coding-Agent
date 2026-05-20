def rearange_string(S):
    from collections import Counter
    import heapq
    
    freq = Counter(S)
    max_freq = max(freq.values())
    if max_freq > (len(S) + 1) // 2:
        return ""
    
    # max heap: store (-freq, char) so that highest frequency comes first
    heap = [(-cnt, ch) for ch, cnt in freq.items()]
    heapq.heapify(heap)
    
    res = []
    prev_char = None
    prev_freq = 0
    
    while heap:
        neg_cnt, ch = heapq.heappop(heap)
        res.append(ch)
        # If there was a previous character with remaining count, push it back
        if prev_freq > 0:
            heapq.heappush(heap, (-prev_freq, prev_char))
        prev_char = ch
        prev_freq = -neg_cnt - 1  # decrease count by 1 after using
    
    return ''.join(res)
