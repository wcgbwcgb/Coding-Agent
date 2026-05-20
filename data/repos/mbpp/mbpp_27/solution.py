def remove(list):
    return [''.join(ch for ch in s if not ch.isdigit()) for s in list]
