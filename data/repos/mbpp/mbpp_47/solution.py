def compute_Last_Digit(A,B):
    result = 1
    for i in range(A+1, B+1):
        result = (result * (i % 10)) % 10
        if result == 0:
            break
    return result
