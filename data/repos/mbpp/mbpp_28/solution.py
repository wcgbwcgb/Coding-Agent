def binomial_Coeff(n,k):
    if k > n - k:
        k = n - k
    res = 1
    for i in range(k):
        res = res * (n - i) // (i + 1)
    return res
