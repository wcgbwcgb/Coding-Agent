def min_length_list(input_list):
    shortest = min(input_list, key=lambda x: len(x))
    return (len(shortest), shortest)
