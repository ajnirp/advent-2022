def priority(char):
    if 'a' <= char <= 'z':
        return ord(char) - ord('a') + 1
    return ord(char) - ord('A') + 27

def common2(s1, s2):
    for c in s1:
        if c in s2:
            return c

def common3(s1, s2, s3):
    for c in s1:
        if c in s2 and c in s3:
            return c

with open('../data/3.txt', 'r') as f:
    data = f.readlines()
    result_1 = 0
    for line in data:
        line = line.strip()
        mid = len(line) // 2
        first, second = line[:mid], line[mid:]
        result_1 += priority(common2(first, second))
    print(result_1)

    result_2 = 0
    # look at 3 lines at a time
    for i in range(len(data)//3):
        lines = [line.strip() for line in data[3*i:3*i+3]]
        result_2 += priority(common3(*lines))
    print(result_2)
