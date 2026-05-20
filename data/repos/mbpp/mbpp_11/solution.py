def remove_Occ(s,ch):
    if ch not in s:
        return s
    first = s.index(ch)
    last = s.rindex(ch)
    if first == last:
        return s[:first] + s[first+1:]
    return s[:first] + s[first+1:last] + s[last+1:]
