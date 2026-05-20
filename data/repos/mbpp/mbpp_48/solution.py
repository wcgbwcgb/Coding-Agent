def odd_bit_set_number(n: int) -> int:
    mask = 0
    for i in range(0, n.bit_length(), 2):
        mask |= 1 << i
    return n | mask
