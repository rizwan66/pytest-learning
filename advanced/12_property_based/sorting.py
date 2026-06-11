def bubble_sort(lst: list) -> list:
    arr = lst[:]
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def merge_sort(lst: list) -> list:
    if len(lst) <= 1:
        return lst[:]
    mid = len(lst) // 2
    left = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])
    return _merge(left, right)


def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def encode_run_length(s: str) -> str:
    """'aaabbc' -> '3a2b1c'"""
    if not s:
        return ""
    result = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            result.append(f"{count}{s[i-1]}")
            count = 1
    result.append(f"{count}{s[-1]}")
    return "".join(result)


def decode_run_length(s: str) -> str:
    """'3a2b1c' -> 'aaabbc'"""
    result = []
    i = 0
    while i < len(s):
        count = int(s[i])
        result.append(s[i + 1] * count)
        i += 2
    return "".join(result)
