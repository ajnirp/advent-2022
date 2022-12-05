def parse_range(r):
    a, b = r.split('-')
    return (int(a), int(b))

# True iff [x1, y1] lies within [x2, y2]
# Overlaps permitted i.e. x1 == x2 and/or y1 == y2
def strict_subset(r1, r2):
    x1, y1 = r1
    x2, y2 = r2
    return x2 <= x1 and y1 <= y2

# True iff r1 and r2 overlap
def overlap(r1, r2):
    x1, y1 = r1
    x2, y2 = r2
    return x2 <= x1 <= y2 or x2 <= y1 <= y2 or strict_subset(r2, r1)

with open('4.txt', 'r') as f:
    data = f.readlines()
    result_1, result_2 = 0, 0
    for line in data:
        r1, r2 = line.strip().split(',')
        r1 = parse_range(r1)
        r2 = parse_range(r2)
        if strict_subset(r1, r2) or strict_subset(r2, r1):
            result_1 += 1
        if overlap(r1, r2):
            result_2 += 1
    print(result_1, result_2)