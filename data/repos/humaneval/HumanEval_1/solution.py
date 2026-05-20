from typing import List


def separate_paren_groups(paren_string: str) -> List[str]:
    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    """
    # Remove spaces
    s = paren_string.replace(' ', '')
    groups = []
    balance = 0
    current = []
    for ch in s:
        current.append(ch)
        if ch == '(':
            balance += 1
        else:  # ch == ')'
            balance -= 1
        if balance == 0:
            groups.append(''.join(current))
            current = []
    return groups
