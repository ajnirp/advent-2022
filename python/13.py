from collections import Counter, defaultdict
from functools import cmp_to_key

def parse_pair(pair):
    a, b = pair.split('\n')
    return eval(a), eval(b)

# -1 a smaller
# 0 eq
# 1 b smaller
def compare(a, b):
    i, j = 0, 0
    while True:
        if i == len(a) and j == len(b): return 0
        elif i == len(a) and j < len(b): return -1
        elif i < len(a) and j == len(b): return 1
        elif type(a[i]) == int and type(b[j]) == int:
            if a[i] == b[j]: i, j = i+1, j+1
            elif a[i] < b[j]: return -1
            else: return 1
        elif type(a[i]) == int and type(b[j]) == list:
            recur = compare([a[i]], b[j])
            if recur == 0: i, j = i+1, j+1
            else: return recur
        elif type(a[i]) == list and type(b[j]) == int:
            recur = compare(a[i], [b[j]])
            if recur == 0: i, j = i+1, j+1
            else: return recur
        else:
            recur = compare(a[i], b[j])
            if recur == 0: i, j = i+1, j+1
            else: return recur

with open('../data/13.txt', 'r') as f:
    data = f.read().strip().split('\n\n')
    data = [parse_pair(pair) for pair in data]

    result = sum(i+1 for i, pair in enumerate(data) if compare(*pair) != 1)
    print(result)

    divider = [[[2]], [[6]]]
    packets = []
    for pair in data:
        packets.append(pair[0])
        packets.append(pair[1])
    for packet in divider:
        packets.append(packet)

    packets.sort(key=cmp_to_key(compare))
    i1 = next(i+1 for i, p in enumerate(packets) if compare(p, divider[0]) == 0)
    i2 = next(i+1 for i, p in enumerate(packets) if compare(p, divider[1]) == 0)
    print(i1*i2)