def find_Max_Num(arr,n) :
    arr.sort(reverse=True)
    return int(''.join(map(str, arr)))
