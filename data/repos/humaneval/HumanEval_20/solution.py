from typing import List, Tuple


def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
    """ From a supplied list of numbers (of length at least two) select and return two that are the closest to each
    other and return them in order (smaller number, larger number).
    >>> find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.2])
    (2.0, 2.2)
    >>> find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.0])
    (2.0, 2.0)
    """
    numbers_sorted = sorted(numbers)
    best_pair = (numbers_sorted[0], numbers_sorted[1])
    best_diff = abs(numbers_sorted[1] - numbers_sorted[0])
    for i in range(len(numbers_sorted) - 1):
        diff = abs(numbers_sorted[i + 1] - numbers_sorted[i])
        if diff < best_diff:
            best_diff = diff
            best_pair = (numbers_sorted[i], numbers_sorted[i + 1])
    return best_pair
