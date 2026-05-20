def max_len_sub(arr, n):
    dp = {}
    max_len = 0
    for x in arr:
        best = 0
        for v in (x-1, x, x+1):
            if v in dp and dp[v] > best:
                best = dp[v]
        dp[x] = best + 1
        if dp[x] > max_len:
            max_len = dp[x]
    return max_len
