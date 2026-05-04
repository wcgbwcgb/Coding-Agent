def remove(list):
    return [''.join(c for c in s if not c.isdigit()) for s in list]
