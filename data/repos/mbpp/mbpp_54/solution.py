def counting_sort(my_list):
    if not my_list:
        return []
    min_val = min(my_list)
    max_val = max(my_list)
    range_of_elements = max_val - min_val + 1
    count = [0] * range_of_elements
    for num in my_list:
        count[num - min_val] += 1
    sorted_list = []
    for i in range(range_of_elements):
        sorted_list.extend([min_val + i] * count[i])
    return sorted_list
