def find_missing(ar,N):
    for i, val in enumerate(ar):
        if val != i + 1:
            return i + 1
    return len(ar) + 1
